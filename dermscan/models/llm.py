import click
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class LLM:
    def __init__(self, model="llama3"):
        self.model = Ollama(model="llama3")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an intelligent agent capable of identifying the primary skincare product and relevant skincare ingredients from HTML pages.",
                ),
                (
                    "human",
                    "Can you help me identify the primary skincare product and relevant skincare ingredients from these HTML contents? I fetched them from a website.",
                ),
                (
                    "ai",
                    "Sure, I can help you with that. First, how would you like me to format the output to your inquiry?",
                ),
                (
                    "human",
                    "I'd like you to print the name of the skincare product and return a list of skincare ingredients normalized to lower case.",
                ),
                (
                    "ai",
                    "Understood. I will return the name of the skincare product and a list of skincare ingredients. Please provide me with the HTML contents of the page that you fetched.",
                ),
                ("human", "Here is the HTML content of the page: {user_input}"),
                (
                    "ai",
                    "I have identified the primary skincare product and relevant skincare ingredients. Here is the output: <output>",
                ),
            ]
        )
        self.chain = self.prompt | self.model | StrOutputParser()

    def invoke(self, text: str) -> str:
        """
        Generate a list of skincare ingredients from a given text.

        Parameters:
        - text (str): The input text to generate the list of ingredients.

        Returns:
        - str: A list of skincare ingredients.
        """
        response = self.chain.invoke({"user_input": text})
        click.echo("Returned LLM response:")
        click.echo(response)
        return response
