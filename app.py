
import streamlit as st
from database import DatabaseManager
from chatbot_logic import ChatbotLogic
from rag_pipeline import RAGPipeline
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Google API key
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    st.error("Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown(f'''
<style>
    .stApp {{
        background-color: #0E1117;
        color: #FAFAFA;
    }}
    [data-testid="stChatMessage"] {{
        background-color: #262730;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.1);
    }}
    [data-testid="stChatMessage"] p {{
        margin: 0;
    }}
    .st-emotion-cache-1c7y2kd {{
        color: #4F8BF9; /* User icon color */
    }}
    .st-emotion-cache-4oy321 {{
        color: #2DBF7A; /* Assistant icon color */
    }}
    [data-testid="stTextInput"] {{
        border-radius: 8px;
        border: 1px solid #3D3F48;
        background-color: #1A1C22;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}
    h1 {{
        color: #FAFAFA;
        text-align: center;
    }}
    .subtitle {{
        text-align: center;
        color: #A0A0A0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}
</style>
''', unsafe_allow_html=True)

# --- Page Title and Description ---
st.markdown('<h1>Grievance Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI-powered assistant for registering complaints and getting answers.</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">You can <b>file a new complaint</b>, ask for the <b>status of an existing one</b>, or ask <b>questions about our policies</b> from the knowledge base.</p>', unsafe_allow_html=True)


# Initialize components
db_manager = DatabaseManager("grievances.db")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
rag_pipeline = RAGPipeline("knowledge_base", embeddings)
chatbot_logic = ChatbotLogic(db_manager, rag_pipeline)



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chatbot_logic.handle_message(st.session_state, prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
