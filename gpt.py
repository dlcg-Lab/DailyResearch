import time

import openai

# 确保你的config.py文件中包含正确的api_base, api_key和model。
from config import api_base, api_key, model


class LLMConstructor:
    def __init__(self):
        self.api_base = api_base
        self.api_key = api_key
        self.model = model

        openai.api_base = self.api_base
        openai.api_key = self.api_key

        print(f"OpenAI Config:{self.model}")

    def get_papers_summary(self, titles, summaries):
        system_message = (
            f"Based on the given paper titles and abstracts, today's Daily Computer Graphics and Deep Learning paper "
            f"digest is generated around 300 Chinese characters, including a summary of key content, "
            f"exploration of research directions, and prospects for the future."
        )
        titles_and_summaries = [f"{title}: {summary}" for title, summary in zip(titles, summaries)]
        user_message = "\n".join(titles_and_summaries)

        response = self.send_message(system_message, user_message, True)

        return response

    def get_paper_summary(self, title, abstract, keywords):
        # System message in English asking for output in the specified format
        system_message = (
            "Your task is to analyze the input paper. "
            "Check if the topic of the paper is related to any of the following fields: "
            f"{keywords}."
            "If the paper does not relate to these fields, reply with 'Not@@CG@@DL'. "
            "If the paper is related, provide three pieces of information: "
            "1. Translate the title into Chinese. "
            "2. Provide a summary of the abstract in Chinese, limited to 50 characters. "
            "3. Translate the entire abstract into Chinese. "
            "Format your response as follows: 'Translated Title@@Chinese Summary@@Translated Abstract'."
        )

        # User message is the paper's title and abstract
        user_message = f"{title}@@{abstract}"

        # Initialize an empty response
        response = ""

        # Attempt to get a correctly formatted response
        while True:
            # Call send_message method and pass the defined system message and user message
            response = self.send_message(system_message, user_message)

            print("current response:", response)
            # Try to split the response and retry if unsuccessful
            try:
                title_translation, summary, abstract_translation = response.split('@@')
                print("Analysing the paper successful.")
                # Break the loop if splitting is successful
                break
            except ValueError:
                # If splitting is unsuccessful, print an error message and continue the loop
                print("Error splitting response, retrying...")

        return title_translation.strip(), summary.strip(), abstract_translation.strip()

    def send_message(self, system_message, user_message, use_gpt_4=False):
        md = self.model
        if use_gpt_4:
            md = 'gpt-4'
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=md,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")
                time.sleep(1)  # Wait for 1 second before retrying


if __name__ == "__main__":
    # Replace 'Your Title Here' and 'Your Abstract Here' with the actual title and abstract.
    llm = LLMConstructor()
