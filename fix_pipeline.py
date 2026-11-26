with open("core/rag_pipeline.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Remove old duplicate body (lines 359 to 521, 0-indexed 358 to 520)
# Keep everything before line 359 and after line 521
cleaned = lines[:358] + lines[521:]

with open("core/rag_pipeline.py", "w", encoding="utf-8") as f:
    f.writelines(cleaned)

print("Done. Total lines:", len(cleaned))
