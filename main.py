import os
from datetime import datetime
import argparse
import arxiv
import markdown
from gpt import LLMConstructor

# Assume LLMConstructor and its method get_paper_summary are well-defined elsewhere
gpt = LLMConstructor()
client = arxiv.Client()

# Create an instance of ArgumentParser
parser = argparse.ArgumentParser(description='Retrieve papers from arXiv based on given keywords.')
# Add the keywords argument, allowing for multiple values
parser.add_argument('keywords', nargs='+', help='List of keywords to search for.')
# Add the focus argument, allowing for multiple values
parser.add_argument('--focus', nargs='+', required=True, help='Focus terms for the GPT paper summary.')
# Parse the command line arguments
args = parser.parse_args()

# Use the keywords from the arguments as the search query
today_keywords = args.keywords
# Use the focus terms from the arguments for GPT summary
gpt_focus = args.focus  # This will be a list of focus terms

combined_keywords = ' OR '.join(today_keywords)
# The focus terms could be combined into a string if needed, e.g., ' AND '.join(gpt_focus)

combined_focus = ', '.join(gpt_focus)

# Search query with the combined keywords
search = arxiv.Search(
    query=combined_keywords,
    max_results=128,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Initialize lists to store the paper details
paper_details = []

# Get today's date
today_date = datetime.now().strftime('%Y-%m-%d')

# Fetch and analyze papers
print("Fetching today's papers...")
for paper in client.results(search=search):
    if len(paper_details) >= 16:
        break

    paper_summary = gpt.get_paper_summary(paper.title, paper.summary, combined_focus)

    if isinstance(paper_summary, tuple) and len(paper_summary) == 3:
        title_translation, summary, abstract_translation = paper_summary

        if title_translation == "Not" or len(abstract_translation) <= 25:
            continue

        paper_details.append({
            "title": paper.title,
            "url": paper.entry_id,
            "title_translation": title_translation,
            "summary": summary,
            "abstract_translation": abstract_translation
        })

# Generate introduction
titles = [paper['title'] for paper in paper_details]
summaries = [paper['summary'] for paper in paper_details]
introduction = gpt.get_papers_summary(titles, summaries)

# Construct Markdown content
markdown_content = f"""# 今日CG&DL论文速报

{today_date}，今日关键词：{'，'.join(today_keywords)}

{introduction}

---
"""

for paper in paper_details:
    markdown_content += f"""### {paper['title']}

**{paper['title_translation']}**：{paper['summary']}

**论文摘要**：

> {paper['abstract_translation']}

---

"""

# Convert Markdown to HTML
html_content = markdown.markdown(markdown_content)

# Ensure the output directory exists
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Save the Markdown file
md_file_path = os.path.join(output_dir, f"{today_date}-论文速报.md")
with open(md_file_path, 'w', encoding='utf-8') as file:
    file.write(markdown_content)

# Save the HTML file with CSS (optional)
css_file_path = 'github.css'
with open(css_file_path, 'r', encoding='utf-8') as css_file:
    css_content = css_file.read()
html_content_with_style = f"<html><head><style>{css_content}</style></head><body>{html_content}</body></html>"

# The saving of the HTML file is not shown, but you would write the html_content_with_style variable to an .html file.
