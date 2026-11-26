with open("core/rag_pipeline.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find and replace the old _page_query_stream body
# by fixing the "Diagram Analysis" yield line
old = 'yield "## \U0001f5bc\ufe0f Page Analysis\\n\\n"'
new = 'yield "## \U0001f4c4 Page Analysis\\n\\n"'
content = content.replace(old, new)

# Also fix any remaining diagram analysis header
old2 = 'yield "## \U0001f5bc\ufe0f Diagram Analysis\\n\\n"'
new2 = 'yield "## \U0001f4c4 Page Analysis\\n\\n"'
content = content.replace(old2, new2)

with open("core/rag_pipeline.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed")
