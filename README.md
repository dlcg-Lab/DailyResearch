# arXiv Daily Paper Digest

## Overview
This project is a Python script that retrieves the latest papers from the arXiv repository based on specific keywords. It leverages the `arxiv` library to fetch papers and uses the `openai` library to generate summaries for each paper using the GPT (Generative Pretrained Transformer) model. The script outputs the results in both Markdown and HTML format.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.6 or higher.
- You have an OpenAI API key for using GPT model capabilities.

## Installation
To install the required libraries, run the following command:

```bash
pip install arxiv openai markdown
```

## Configuration

After cloning the repository, you will need to set up your environment. Open `config.py` and fill in your OpenAI API key.

## Usage

To run the script, use the following command:

```cmd
python main.py "keyword1" "keyword2" --focus "focus1" "focus2" "focus3"
```

Replace `"keyword1" "keyword2"` with your targeted search keywords for papers, and replace `"focus1" "focus2" "focus3"` with your focus terms for GPT paper summarization.

## CSS Styling
We have applied a styling using CSS from a Gist by xiaolai. To include this styling:
Download the CSS from xiaolai's gist.
Save it as github.css in the root directory of the project.

## Output

The script generates two files in the `output` directory:

1. A Markdown file (`YYYY-MM-DD-论文速报.md`) containing the digest of the papers.
2. An HTML file (`YYYY-MM-DD-论文速报.html`) formatted with the included CSS file(if in need).

## Contribution

Contributions to this project are welcome. Please feel free to fork the repository and submit a pull request.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

If you have any questions or feedback, please contact the project maintainer at Chenlizheme@outlook.com
