import ollama
import os
import mlflow
from app.rag.retriever import hybrid_search
from app.services.evaluator import evaluate

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("RAG_Pipeline")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

LLM_CONFIG = {
    "model": "llama3",
    "temperature": 0.0,
    "top_p": 0.9,
    "top_k": 40,
    "num_predict": 2000
}

SYSTEM_PROMPT = """
Tu es CliniQ, Tu dois répondre UNIQUEMENT avec les informations du CONTEXTE ci-dessous.

RÈGLES ABSOLUES:
1. COPIE INTÉGRALEMENT toutes les informations pertinentes du CONTEXTE
2. NE RÉSUME PAS - donne TOUTES les informations disponibles
3. NE JAMAIS ajouter d'informations qui ne sont pas dans le contexte
4. NE JAMAIS utiliser tes connaissances générales
5. Si plusieurs informations sont pertinentes, LISTE-LES TOUTES sans exception
6. Si l'information n'est PAS dans le contexte: "Cette information n'est pas disponible dans ma documentation."

CONTEXTE (5 documents trouvés - utilise TOUS ceux qui sont pertinents):
{context}

Question: {question}
La réponse doit être rédigée sous forme de texte fluide et naturel, comme si elle venait d’un assistant intelligent.

Commence toujours par :
"Bonjour 👋, voici ce que j’ai trouvé pour vous :"

Ensuite :

Reformule les informations du contexte de manière claire et structurée.

Utilise un ton professionnel et amical.

Intègre naturellement les informations au lieu de faire une simple liste brute.

Ensuite, rédige uniquement les informations disponibles dans le contexte, en copiant ou reformulant strictement ce qui est écrit.

⚠️ Ne jamais ajouter d’exemples, de causes possibles, ni de recommandations personnelles."""

def generate(question: str, evaluate: bool = False, k: int = 5) -> str:
    chunks = hybrid_search(question, k) or []
    retrieval_context = [c.get("content", "") for c in chunks]
    context = "\n\n---\n\n".join(retrieval_context)

    client = ollama.Client(host=OLLAMA_HOST)
    full_prompt = SYSTEM_PROMPT.format(context=context, question=question)

    response = client.chat(
        model=LLM_CONFIG["model"],
        messages=[
            {"role": "system", "content": "Tu es un assistant clinique strict basé sur RAG."},
            {"role": "user", "content": full_prompt}
        ],
        options={
            "temperature": LLM_CONFIG["temperature"],
            "top_p": LLM_CONFIG["top_p"],
            "top_k": LLM_CONFIG["top_k"],
            "num_predict": LLM_CONFIG["num_predict"]
        }
    )

    answer = response["message"]["content"].replace("\n", " ")
    return answer


def generate_and_evaluate(question: str, k: int = 5):
    with mlflow.start_run(run_name="rag_pipeline"):

        mlflow.log_params(LLM_CONFIG)
        mlflow.log_param("k", k)

        chunks = hybrid_search(question, k) or []
        answer = generate(question, k=k)

        metrics = evaluate(question, answer, chunks, k=k)

        return answer, metrics


