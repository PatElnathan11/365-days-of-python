import os
import re

CSS_TEMPLATE = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #e1e4e8;
        background-color: #0d1117;
        max-width: 800px;
        margin: 40px auto;
        padding: 0 20px;
    }
    h1, h2, h3 { color: #58a6ff; border-bottom: 1px solid #21262d; padding-bottom: 0.3em; }
    code { background: #161b22; padding: 0.2em 0.4em; border-radius: 6px; font-family: monospace; color: #f0883e; }
    pre { background: #161b22; padding: 16px; border-radius: 6px; overflow-x: auto; }
    pre code { background: none; padding: 0; color: #e1e4e8; }
    a { color: #58a6ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    ul { padding-left: 20px; }
    li { margin-bottom: 4px; }
    blockquote { border-left: 4px solid #30363d; color: #8b949e; padding-left: 16px; margin: 0; }
</style>
"""

def parse_markdown(md_text: str) -> str:
    """Mengonversi sintaks Markdown menjadi tag HTML."""
    lines = md_text.splitlines()
    html_lines = []
    in_code_block = False
    in_list = False

    for line in lines:
        # 1. Handle Code Blocks (```)
        if line.strip().startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                html_lines.append("<pre><code>")
                in_code_block = True
            continue

        if in_code_block:
            # Escape HTML di dalam blok kode
            escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_lines.append(escaped_line)
            continue

        # 2. Close List jika baris bukan list
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item_text = line.strip()[2:]
            html_lines.append(f"  <li>{item_text}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False

        # Ignore empty lines
        if not line.strip():
            continue

        # 3. Headings
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
            continue
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
            continue
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
            continue

        # 4. Inline Elements (Bold, Italic, Inline Code, Links)
        # Bold: **text**
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        # Italic: *text*
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        # Inline Code: `code`
        line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
        # Link: [text](url)
        line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank">\1</a>', line)

        html_lines.append(f"<p>{line}</p>")

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)

def convert_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    body_html = parse_markdown(md_content)

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Document</title>
    {CSS_TEMPLATE}
</head>
<body>
{body_html}
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def main():
    print("==============================================")
    print(" MARKDOWN TO HTML CONVERTER (Day 010) ")
    print("==============================================")

    input_file = "sample.md"
    output_file = "output.html"

    if not os.path.exists(input_file):
        print(f"File '{input_file}' tidak ditemukan!")
        return

    print(f"Mengonversi '{input_file}' -> '{output_file}'...")
    convert_file(input_file, output_file)
    print(f"Berhasil! Buka file '{output_file}' di browser untuk melihat hasilnya.\n")

if __name__ == "__main__":
    main()