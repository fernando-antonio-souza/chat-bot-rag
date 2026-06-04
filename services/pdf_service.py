import os
import tempfile


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

# Função que processa o pdf. cria um pdf temporário na memória e depois o remove
def process_pdf(file):

    # Cria o arquivo temporário
    try:
        with tempfile.NamedTemporaryFile(delete= False, suffix= ".pdf") as temp_file:

            temp_file.write(file.read())
            temp_path = temp_file.name

        # Carrega o caminho do pdf
        loader = PyPDFLoader(temp_path)

        # Cria o doc do pdf
        docs = loader.load()

        # Remove o pdf da memória
        os.remove(temp_path)

        # Cria os chunks sobre os dados do pdf
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = CHUNK_SIZE,
            chunk_overlap= CHUNK_OVERLAP,
        )

        return text_splitter.split_documents(docs)
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise Exception(f"Falha ao processar o PDF: {e}")
