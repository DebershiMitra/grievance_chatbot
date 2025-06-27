# Grievance Management RAG Chatbot

This project is a sophisticated, RAG-based chatbot designed for grievance registration and status tracking. It leverages a Large Language Model (LLM) to provide intelligent, context-aware responses and interacts with a local database to manage complaint data persistently.

## Key Features

- **Conversational UI**: A clean and modern chat interface built with Streamlit.
- **RAG Pipeline**: Uses a Retrieval-Augmented Generation (RAG) pipeline with LangChain and ChromaDB to answer user questions based on a custom knowledge base (e.g., `customer_service_faqs.pdf`).
- **Intelligent Intent Recognition**: Accurately determines the user's intent (registering a complaint, checking status, or asking a general question) using a robust prompting strategy.
- **Stateful Conversations**: Remembers the context of the conversation to ask follow-up questions and collect all necessary user details (name, phone, email) before registering a complaint.
- **Secure API Key Management**: Uses a `.env` file to securely manage the Google API key, which is ignored by Git to prevent accidental exposure.
- **Persistent Storage**: All registered grievances are stored in a local SQLite database (`grievances.db`).

## Technology Stack

- **Application Framework**: Streamlit
- **Language**: Python
- **LLM & AI**: Google Gemini, LangChain
- **Vector Store**: ChromaDB
- **Database**: SQLite
- **Dependency Management**: Conda & Pip

## Project Structure

```
grievance_chatbot/
|-- .env                    # Stores secret keys (e.g., GOOGLE_API_KEY)
|-- .gitignore              # Specifies files for Git to ignore
|-- app.py                  # Main Streamlit application file (UI and session management)
|-- chatbot_logic.py        # Core conversational logic, state management, and LLM calls
|-- database.py             # Handles all SQLite database operations
|-- rag_pipeline.py         # Logic for creating and querying the RAG vector store
|-- requirements.txt        # Project dependencies
|-- knowledge_base/
|   |-- customer_service_faqs.pdf # The custom knowledge base document
|-- grievances.db           # The SQLite database file 
|-- README.md               # This file
```

## Setup and Installation Guide

Follow these steps to set up and run the project locally.

### Prerequisites
- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.
- [Git](https://git-scm.com/downloads) installed.

### 1. Create and Activate the Conda Environment

This project requires a specific set of dependencies. To avoid conflicts with your existing Python packages, you must run it in an isolated Conda environment.

```bash
# Create a new Conda environment named 'chatbot-env' with Python 3.11
conda create -n chatbot-env python=3.11 -y

# Activate the newly created environment
conda activate chatbot-env
```

### 2. Set Up the `.env` File

The application requires a Google API key to function. Create a file named `.env` in the root of the `grievance_chatbot` folder and add your key:

```
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

### 3. Install Dependencies

With the `chatbot-env` environment active, install all the required Python packages using the `requirements.txt` file.

```bash
# Navigate to the project directory if you are not already there
cd path/to/grievance_chatbot

# Install all dependencies
pip install -r requirements.txt
```

## Running the Application

Once the setup is complete, you can run the application with a single command from your terminal (make sure the `chatbot-env` is still active).

```bash
streamlit run app.py
```

The application will open in your default web browser, ready for you to interact with.

## How to Use the Chatbot

- **To Register a Complaint**: Simply state your intention, e.g., "I want to file a complaint." The bot will guide you through the process of collecting your details.
- **To Check Status**: Ask about the status and provide your complaint ID when prompted, e.g., "What's the status of my complaint?"
- **To Ask a Question**: Ask any question related to the information in the `customer_service_faqs.pdf`, e.g., "What is the return policy?"
