from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from blog_api import search_blog, crawl_blog
from examples import keywords

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
vdb = Chroma(persist_directory=".", embedding_function=embeddings)

def update_vdb(keywords):
    load_dotenv()

    links = []
    result = search_blog(keywords, length=20, sort='sim')

    for item in result['items']:
        links.append(item['link'])

    docs = []
    for link in links:
        doc = crawl_blog(link)
        docs.append(Document(page_content=doc, metadata={"source": link}))
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)

    vdb.add_documents(split_docs)

    return vdb

#update_vdb(keywords) #test update_vdb() function