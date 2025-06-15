from abc import ABC, abstractmethod

from lightrag.core.generator import Generator
from lightrag.core.component import Component
from lightrag.core.model_client import ModelClient
from lightrag.components.model_client import OllamaClient, GroqAPIClient
from openai import OpenAI


class Model(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self, input_code: str) -> str:
        pass


class DummyModel(Model):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def run(self, input_code: str) -> str:
        return input_code


qa_template = r"""<SYS>
Your answer will be written to the file "newcode.py" Please, write python code as answer. Imagine that you are an oilman who has been given the task of reverse engineering hydraulic correlations. You were given a c++ code where the designation of variables is unclear, but you can use the formula to understand what this variable is. Decode these variables. Rewrite the following math code: rename variables, create new variables for constants as pi and other, make it easy-readable. Write code only as answer.
</SYS>
User:  {{input_str}}
You:"""


class SimpleQA(Component):
    def __init__(self, model_client: ModelClient, model_kwargs: dict):
        super().__init__()
        self.generator = Generator(
            model_client=model_client,
            model_kwargs=model_kwargs,
            template=qa_template,
        )

    def call(self, input):
        return self.generator.call({"input_str": str(input)})

    async def acall(self, input: dict):
        return await self.generator.acall({"input_str": str(input)})


class Codellama(Model):
    def __init__(self):
        model = {"model_client": OllamaClient(), "model_kwargs": {"model": "codellama:13b"}}
        self.component = SimpleQA(**model)

    def run(self, code: str) -> str:
        output = self.component.call(code).data
        print(output)
        return output


class Phi4(Model):
    def __init__(self):
        model = {"model_client": OllamaClient(), "model_kwargs": {"model": "phi4:14b"}}
        self.component = SimpleQA(**model)

    def run(self, code: str) -> str:
        output = self.component.call(code).data
        print(output)
        return output


class OpenAIModel(Model):
    def __init__(self):
        self.client = OpenAI()

    def run(self, code: str) -> str:
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": "rewrite following math code with clear naming. Write code only as answer. \n" + code}],
            stream=False,
        )
        answer = stream.choices[0].message.content
        return answer


class DeepSeekModel(Model):
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.completion = None

    def run(self, input_code: str) -> str:
        self.completion = self.client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {
                    "role": "user",
                    "content": "Please provide only the code as output. The code should include the following modifications:   All original mathematical expressions should be decrypted or made explicit (e.g., simplify encoded formulas or clarify any mathematical logic).    All variable names should be renamed to meaningful names based on their purpose.    All class names should be changed by appending _new to the original name (e.g., ClassB -> ClassB_new).    Function names must remain unchanged.    Add full documentation (docstrings and comments) to explain the purpose and logic of the code. Do not include any text outside of the code block. Please write working code as content (even if not fully decrypted), you don't have to write explanation.\n" + input_code
                }
            ],
            stream=False,
        )

        answer = self.completion.choices[0].message.content
        return answer


