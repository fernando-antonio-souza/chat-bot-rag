from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough

from prompts.rag_prompt import RAG_SYSTEM_PROMPT


class RAGService:

    def __init__(self, model_name, vector_store):
        self.model_name = model_name
        self.vector_store= vector_store


    def format_docs(self, docs):

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )
    
    def ask(self, question, messages):
        try:
            llm = ChatOpenAI(
                model= self.model_name
            )

            retriever = (
                self.vector_store.as_retriever(search_kwargs= {"k":4})
            )

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", RAG_SYSTEM_PROMPT),

                    *[
                        (
                            msg["role"],
                            msg["content"]
                        )
                        for msg in messages
                    ],

                    ("human", "{input}")
                ]
            )

            rag_chain = (
                {
                    "context": retriever | self.format_docs,
                    "input": RunnablePassthrough(),
                }
                | prompt
                | llm
                | StrOutputParser()
            )

            return rag_chain.invoke(question)
        except Exception as e:
            return f"Erro ao consultar os documentos: {e}"