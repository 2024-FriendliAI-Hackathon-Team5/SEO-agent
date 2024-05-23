from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.friendli import ChatFriendli
from langchain_core.runnables import RunnablePassthrough
from prompt import rag_prompt
from database import vdb
from dotenv import load_dotenv
import os
from examples import title_input, content_input

load_dotenv()

llm = ChatFriendli(
    friendli_token = os.getenv("FRIENDLI_TOKEN"),
    friendli_team= os.getenv("FRIENDLI_TEAM"),
    model = "meta-llama-3-70b-instruct",
    streaming = False,
    # temperature=0.5,
    # max_tokens=100,
    # top_p=0.9,
    # frequency_penalty=0.0,
    # stop=["\n"],
)

def run_rag_chain(title_input, content_input):
    retriever = vdb.as_retriever()

    prompt = PromptTemplate.from_template(rag_prompt, title=title_input, content=content_input)

    rag_chain = (
        {"context": retriever , "content": RunnablePassthrough() }
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(title_input + content_input)
    return result

#print(run_rag_chain(title_input, content_input)) # test run_rag_chain() function