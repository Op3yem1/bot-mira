#import streamlit
import streamlit as st
import os
from dotenv import load_dotenv

# import pinecone
from pinecone import Pinecone, ServerlessSpec

# import langchain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()
# About
st.title("Mira")
st.subheader("A Retrieval-Augmented Generation Chatbot for Ope Johnson's CV")
st.markdown("This chatbot uses Ope Johnson's CV to answer questions about her work experience and educational background. It is powered by LangChain, Pinecone, and OpenAI.")

# initialize pinecone database
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# initialize pinecone database
index_name = os.environ.get("PINECONE_INDEX_NAME")  # change if desired
index = pc.Index(index_name)

# initialize embeddings model + vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ.get("OPENAI_API_KEY"))
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

    st.session_state.messages.append(SystemMessage("You are an assistant, called Mira, that helps potential hirers learn more about Ope Johnson's work experience and background. You may refer to her as Ope or Opeyemi in your responses. Politely decline to answer questions that are not related to her work experience, educational background or that can be found from the provided context."))

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# create the bar where we can type messages
prompt = st.chat_input("Hi, I'm Mira, Ope's assistant. How can I help?")

# did the user submit a prompt?
if prompt:

    # add the message from the user (prompt) to the screen with streamlit
    with st.chat_message("user"):
        st.markdown(prompt)

        st.session_state.messages.append(HumanMessage(prompt))

    # initialize the llm
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=1
    )

    # creating and invoking the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.5},
    )

    docs = retriever.invoke(prompt)
    docs_text = "".join(d.page_content for d in docs)

    # creating the system prompt
    system_prompt = """You are an assistant, called Mira, that helps potential hirers learn more about Ope Johnson's work experience and background. Only refer to her as Ope or Opeyemi in your responses. Politely decline to answer questions that are not related to her work experience, educational background or that can not be found from the provided context. 
    Use three sentences maximum and keep the answer concise.
    Context: {context}:"""

    # Populate the system prompt with the retrieved context
    system_prompt_fmt = system_prompt.format(context=docs_text)


    print("-- SYS PROMPT --")
    print(system_prompt_fmt)

    # adding the system prompt to the message history
    st.session_state.messages.append(SystemMessage(system_prompt_fmt))

    # invoking the llm
    result = llm.invoke(st.session_state.messages).content

    # adding the response from the llm to the screen (and chat)
    with st.chat_message("assistant"):
        st.markdown(result)

        st.session_state.messages.append(AIMessage(result))
