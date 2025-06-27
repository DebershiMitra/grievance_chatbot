
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

class RAGPipeline:
    def __init__(self, knowledge_base_path, embeddings):
        self.knowledge_base_path = knowledge_base_path
        self.embeddings = embeddings
        self.vector_store = self._create_vector_store()

    def _create_vector_store(self):
        loader = PyPDFLoader(os.path.join(self.knowledge_base_path, "customer_service_faqs.pdf"))
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        return Chroma.from_documents(texts, self.embeddings)

    def query(self, question):
        docs = self.vector_store.similarity_search(question)
        return docs[0].page_content if docs else ""
