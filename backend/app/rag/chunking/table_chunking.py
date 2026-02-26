import json

md_file = r"../../data/only_tables.md"
json_output = r"../../data/table_chunks.json"

with open(md_file,"r",encoding="utf-8") as f:
    text = f.read()

def split_into_tables(text):
    tables = []
    for t in text.split("\n---\n"):
        tables.append(t.strip())
    return tables

def parse_table_rows(table_text, table_id):
    lines = [line.rstrip() for line in table_text.split("\n") if line.strip()]
    if not lines:
        return []
    header = [h.strip() for h in lines[0].strip("|").split("|")]
    num_cols = len(header)
    chunks = []
    buffer = ""
    for l in lines[2:]:
        buffer += l + "\n"
        if buffer.count("|") >= num_cols + 1:
            cells = [c.strip().replace("\n"," ") for c in buffer.strip().strip("|").split("|")]
            row = {}
            for i in range(num_cols):
                row[header[i]] = cells[i] if i < len(cells) else ""
            chunks.append({"table_id": table_id, "row": row})
            buffer = ""
    return chunks

def parse_all_tables(text):
    tables = split_into_tables(text)
    all_chunks = []
    for idx, t in enumerate(tables, 1):
        all_chunks.extend(parse_table_rows(t, idx))
    return all_chunks

chunks = parse_all_tables(text)

with open(json_output,"w",encoding="utf-8") as f:
    json.dump(chunks,f,ensure_ascii=False,indent=2)

print("Done")