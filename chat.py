from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models.friendli import ChatFriendli
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from search_blog import search_blog

# 사용자 입력 받기
title_input = "파이썬을 활용한 데이터 분석 - 초보자를 위한 가이드"
content_input = """
데이터 분석은 현대 사회에서 점점 더 중요해지고 있습니다. 기업들은 데이터를 활용하여 의사결정을 내리고, 새로운 인사이트를 도출하며, 비즈니스 성과를 향상시키고 있습니다. 이러한 데이터 분석에 있어서 파이썬은 강력한 도구로 자리잡았습니다.
파이썬은 배우기 쉽고, 다양한 라이브러리를 제공하며, 데이터 분석에 최적화된 환경을 제공합니다. Numpy, Pandas, Matplotlib 등의 라이브러리를 활용하면 데이터를 효과적으로 다룰 수 있습니다.
이 글에서는 파이썬을 활용한 데이터 분석의 기초를 다룹니다. 데이터 로딩, 전처리, 탐색적 데이터 분석(EDA), 시각화 등의 단계를 차근차근 살펴볼 것입니다. 실제 데이터셋을 활용한 예제를 통해 파이썬으로 데이터 분석을 수행하는 방법을 익힐 수 있습니다.
데이터 분석을 시작하는 분들에게 이 글이 유용한 가이드가 되기를 바랍니다. 파이썬의 강력함을 활용하여 데이터에서 가치 있는 인사이트를 발견하고, 데이터 드리븐 의사결정을 내리는 방법을 배워봅시다. 이제 파이썬과 함께 데이터 분석의 세계로 뛰어들어 볼까요? Copy
"""
keywords = ["파이썬", "데이터", "분석"]

load_dotenv()

llm = ChatFriendli(
    friendli_token = os.getenv("FRIENDLI_TOKEN"),
    model = "meta-llama-3-70b-instruct",
    streaming = False,
    # temperature=0.5,
    # max_tokens=100,
    # top_p=0.9,
    # frequency_penalty=0.0,
    # stop=["\n"],
)

links = []
result = search_blog(keywords, length=20, sort='sim')
for item in result['items']:
    links.append(item['link'])

loader = WebBaseLoader(links)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
vdb = Chroma.from_documents(texts, embeddings)
retriever = vdb.as_retriever()

template = """
Referring to the title and content of the given blog post, edit the blog post by refering relevant content.
Write Modified blog post in Korean.

Title: %s
Content: %s

Related content:
{context}

Modified blog post: 
 
""" % (title_input, content_input)

prompt = PromptTemplate.from_template(template, title=title_input, content=content_input)

rag_chain = (
    {"context": retriever}
    | prompt
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke("")
print(result)
