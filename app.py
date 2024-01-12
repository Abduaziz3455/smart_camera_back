import streamlit as st
import os
import sys

from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
import openai

sys.path.append('../..')

load_dotenv(find_dotenv())  # read local .env file

# Initialize OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Initialize OpenAI Embeddings and ChatOpenAI
embedding = OpenAIEmbeddings()
llm_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=llm_name, temperature=0)

# Initialize Chroma Vector Store
persist_directory = 'doc/chroma/'
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Build prompt
template = """Use the following pieces of context to answer the question at the end. If customer wants to contact 
with site admins say "contact via telegram https://t.me/Shahboz_softex" in user's question language. If you don't 
know the answer, say "could you please give more details" in user's question language, don't try to make up an 
answer. Use three sentences maximum. Keep the answer as concise as possible. If the user insults you, warn user do 
not abuse. you're answering to customer who curious with building details. so don't avoid housing topic. if user 
avoid topic warn user with "please, don't get off the main topic". And of course all answers should be in user's 
question language.

{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

# Run chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever(), return_source_documents=True,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})


def main():
    st.title("Chatbot Application")

    # Human Input
    user_input = st.text_input("You:", "")

    # AI Response
    if user_input:
        result = qa_chain({"query": user_input})
        st.text(f"AI: {result['result']}")


if __name__ == "__main__":
    main()
