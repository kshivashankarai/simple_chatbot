import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI 
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnablePassthrough

from operator import itemgetter

load_dotenv()

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

class Conversation:

    def generate_answer(self, question, response):

        llm = ChatOpenAI(
            openai_api_key=os.getenv("GPT_KEY"),
            model_name="gpt-3.5-turbo", 
            temperature=0.5
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions based on the context as best of your ability.",
                ),
                ("placeholder", "{chat_history}"),
                ("human", f"question :{question}\n\nContext: {response}\n\n "),
            ]
        )

        demo_ephemeral_chat_history = ChatMessageHistory()

        trimmer = trim_messages(strategy="last", max_tokens=5, token_counter=len)

        chain_with_trimming = (
            RunnablePassthrough.assign(chat_history=itemgetter("chat_history") | trimmer)
            | prompt
            | llm
        )

        chain_with_trimmed_history = RunnableWithMessageHistory(
            chain_with_trimming,
            lambda session_id: demo_ephemeral_chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        answer = chain_with_trimmed_history.invoke(
            {"input": question},
            {"configurable": {"session_id": "unused"}},
        )

        return answer
