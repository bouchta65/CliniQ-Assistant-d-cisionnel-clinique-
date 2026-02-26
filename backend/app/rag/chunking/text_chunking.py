import json

md_file = r"../../data/only_text.md"
json_output = r"../../data/text_chunks.json"


def chunk_markdown_by_title(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        pages = f.read().split("\n---\n")

    all_chunks = []

    for page_number, page in enumerate(pages, 1):
        lines = page.split("\n")
        current_title = None
        current_content = []

        for line in lines:
            line = line.strip()

            if line.startswith("#"):
                if current_title and current_content:
                    all_chunks.append({
                        "title": current_title.replace("#", "").strip(),
                        "content": "\n".join(current_content).strip(),
                        "page": page_number
                    })

                current_title = line
                current_content = []

            elif current_title:
                if line != "":
                    current_content.append(line)

        if current_title and current_content:
            all_chunks.append({
                "title": current_title.replace("#", "").strip(),
                "content": "\n".join(current_content).strip(),
                "page": page_number
            })

    return all_chunks


def add_domain_metadata(chunks):
    for chunk in chunks:
        page = chunk["page"]

        if 1 <= page <= 8:
            chunk["domain"] = "PÉDIATRIE"
        elif 9 <= page <= 37:
            chunk["domain"] = "MÉDECINE ADULTE"
        elif 38 <= page <= 48:
            chunk["domain"] = "DENTAIRE"
        else:
            chunk["domain"] = "UNKNOWN"

    return chunks


chunks = chunk_markdown_by_title(md_file)
chunks = add_domain_metadata(chunks)

with open(json_output, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(" JSON with domain metadata created!")