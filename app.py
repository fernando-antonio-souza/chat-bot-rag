import streamlit as st

from dotenv import load_dotenv

from services.pdf_service import process_pdf
from services.vector_store_service import vector_store_load
from services.vector_store_service import vector_store_save_documents
from services.rag_service import RAGService


load_dotenv()


# ======== Layout página =========
st.set_page_config(
    page_title= "Chat PyGPT",
    page_icon= "📄",
)

st.header(
    "🤖 Chat com seus documentos"
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

vector_store = vector_store_load()


with st.sidebar:

    st.header("Upload PDFs")

    uploaded_files = (
        st.file_uploader(
            "Selecione PDFs",
            type= ["pdf"],
            accept_multiple_files= True,
        )
    )

    if uploaded_files:

        if st.button("Processar PDFs"):

            all_chunks = []

            with st.spinner("Processando..."):
                try:

                    for file in uploaded_files:

                        chunks = (process_pdf(file))

                        all_chunks.extend(chunks)

                    vector_store = (vector_store_save_documents(all_chunks, vector_store))

                    st.success("Documentos carregados!")
                except Exception as e:
                    st.error(f"Erro ao processar PDFs: {e}")

    selected_model = st.selectbox(
        "Modelo",
        [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4",
        ]
    )

for message in (st.session_state["messages"]):

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Como  posso ajudar?")

if question:

    if vector_store is None:

        st.error("Envie um PDF primeiro.")

    else:

        with st.chat_message("user"):
            st.markdown(question)

        st.session_state["messages"].append(
            {
                "role": "user",
                "content": question,
            }
        )

        rag = RAGService(
            model_name= selected_model,
            vector_store= vector_store,
        )

        with st.spinner("Pensando..."):
            try:

                response = rag.ask(
                    question,
                    st.session_state["messages"]
                )
            except Exception as e:
                st.error(f"Erro ao obter resposta: {e}")
                reponse = "Desculpe, ocorreu um erro ao processar sua pergunta"

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": response,
            }
        )