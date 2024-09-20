from llama_cpp import Llama
import re


class TextToSql:

    def generate_sql(self, context, query):

        model_path = "/home/shiva/DeveloperDen/Python/chat_with_postgres/model/tinyllama-1.1b-chat-v1.0.Q8_0.gguf"

        llm = Llama(model_path=model_path, n_ctx=512, n_threads=8, n_gpu_layers=40)

        # template = f"""\
        # <|im_start|>user
        # Given the database structure, generate an raw SQL query for the following question
        # database structure:{context}
        # question:{query}
        # <|im_end|>
        # <|im_start|>assistant 
        # """

        template = f"""\
        <|im_start|>user
        Given the context, generate an SQL query for the following question
        context:{context}
        question:{query}
        <|im_end|>
        <|im_start|>assistant 
        """

        template = "\n".join([line.lstrip() for line in template.splitlines()])

        output = llm(template, max_tokens=512, stop=["</s>"])

        text = output['choices'][0]['text']

        return text