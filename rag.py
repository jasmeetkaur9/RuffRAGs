from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
import os
from langchain.agents import create_agent
import faiss
import json
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.agents import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from hybrid_ret import HybridRet

sessions = [] 
ChatHistory_DIR = os.path.join(os.path.dirname(__file__), "threads")

class AgentState(AgentState):
    session_id : str

@dynamic_prompt
def prompt_with_context(request:ModelRequest):

    last_query = request.state["messages"][-1].text
    last_message = request.state["messages"][-1]

    retrieved_docs = vectorstore.similarity_search(last_query, k = 5)
    # retrieved_docs = hy_store.similarity_search(last_query, 3, 6)
    
    content = [] 
    for d in retrieved_docs:
        link_doc = d.metadata.get("link")
        content.append(f"Content: {d.page_content}\n Link: {link_doc}")
    
    docs_content = "\n\n".join(content)

    system_message = (
        "You are a helpful and friendly assistant for answering user queries." 
        "Answer exclusively from the supplied context. "
        "Use the following pieces of retrieved context to answer the question."
        "Stick to answers related to the company's product."
        "If not sure of the how to answer, keep the answer general and strictly within the context."
        "If there is no answer, suggest reaching out to the team."
        "Answer with a positive tone and keep the answer concise. Use a maximum of five sentences."
        f"\n\n{docs_content}"
    )

    return system_message

def get_session_history(thread_id):

    path = os.path.join(ChatHistory_DIR, f"{thread_id}.json")
    if not os.path.exists(path):
        return [] 
    with open(path, "r") as f:
        return json.load(f)

    
def save_thread_history(thread_id, messages):

    os.makedirs(ChatHistory_DIR, exist_ok=True)

    with open(os.path.join(ChatHistory_DIR, f"{thread_id}.json"), "w") as f:
        json.dump(messages, f, indent=2, default=str)

def run_chat(query, session_id, get_session_hist:False):

    hist_messages = get_session_history(session_id)
    v = []
    for step in agent.stream(
        {
            "messages" : [{"role" : "user", "content" : query}],
            "session_id": str(session_id)
        },
        {"configurable": {"thread_id": str(session_id)}},
        stream_mode = "values",
    ):
        v.append(step["messages"][-1].pretty_repr())

    full_conv = hist_messages + v 
    save_thread_history(session_id, full_conv)

    response = v[-1]
    response = response.replace("================================== Ai Message ==================================\n\n", "")

    if get_session_hist:
        return response, full_conv
    else:
        return response, v


model = ChatOllama(model="llama3.1:8b", num_gpu=1)
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800, 
    chunk_overlap = 50
)

embedding_dim = len(embedding_model.embed_query("hello world"))
index = faiss.IndexFlatL2(embedding_dim)

vectorstore = FAISS(
                    embedding_function=embedding_model,
                    index=index,
                    docstore=InMemoryDocstore(),
                    index_to_docstore_id={},
                )


texts = [] 
metadatas = []
docs = []

folder_path = "docs"

for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read()

    meta_part, content = lines.split("---", 1)

    metadata = {}

    for line in meta_part.strip().split("\n"):
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    
    texts.append(content)
    metadatas.append(metadata)
    doc = Document(page_content = content, metadata = metadata)
    docs.append(doc)
        
splits = text_splitter.split_documents(docs)
vectorstore.add_documents(documents=splits)
hy_store = HybridRet(docs, embedding_model)
agent = create_agent(model, tools=[], state_schema=AgentState, checkpointer=InMemorySaver(), middleware=[prompt_with_context])

