# Chat PyGPT — RAG com Streamlit

Chatbot com interface web que permite fazer perguntas sobre documentos PDF usando RAG (Retrieval-Augmented Generation) com OpenAI e ChromaDB.

## Stack

- **Interface:** [Streamlit](https://streamlit.io)
- **LLM:** OpenAI (GPT-4o-mini, GPT-4o, GPT-4)
- **Vector store:** ChromaDB com embeddings OpenAI
- **PDF processing:** LangChain + PyPDFLoader
- **Gerenciador de pacotes:** uv

## Como usar

```bash
# Clonar e acessar o projeto
git clone <url>
cd chatbot_rag

# Criar ambiente virtual e ativar
uv venv
source .venv/bin/activate

# Instalar dependências
uv pip install -r requirements.txt

# Configurar chave da OpenAI
cp .env.example .env
# Edite .env com sua OPENAI_API_KEY

# Rodar
streamlit run app.py
```

## Estrutura

```
├── app.py                    # Interface Streamlit
├── config/
│   └── settings.py           # Configurações (chunk size, persist dir)
├── services/
│   ├── pdf_service.py        # Extração e chunking de PDFs
│   ├── vector_store_service.py  # Persistência no ChromaDB
│   └── rag_service.py        # Chain de busca + resposta com LLM
├── prompts/
│   └── rag_prompt.py         # System prompt do assistente
├── db/                       # Base vetorial persistida (ChromaDB)
├── requirements.txt
└── .env                      # OPENAI_API_KEY (não versionado)
```

## Fluxo

1. Upload de PDFs → extração de texto → divisão em chunks
2. Chunks são embeddados e armazenados no ChromaDB
3. Usuário faz pergunta → busca os 4 chunks mais similares
4. Chunks + pergunta + histórico → GPT → resposta

## Configuração

No `config/settings.py`:

| Variável        | default | descrição                  |
|-----------------|---------|----------------------------|
| `CHUNK_SIZE`    | 1000    | Tamanho de cada chunk      |
| `CHUNK_OVERLAP` | 200     | Sobreposição entre chunks  |
| `PERSIST_DIRECTORY` | `db` | Diretório do ChromaDB      |
