import os
from langchain_google_genai import ChatGoogleGenerativeAI
from database import DatabaseManager
from rag_pipeline import RAGPipeline

class ChatbotLogic:
    def __init__(self, db_manager, rag_pipeline):
        self.db_manager = db_manager
        self.rag_pipeline = rag_pipeline
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    def get_intent(self, user_message):
        prompt = f"""Your task is to classify the user's intent based on their message.
The user is interacting with a grievance registration chatbot.

Here are the possible intents:
- 'register_complaint': The user explicitly asks to create, file, log, or register a new complaint.
- 'check_status': The user wants to know the status of an existing complaint and might provide a complaint ID.
- 'general_question': The user is asking a question about a policy, a product issue, or a general inquiry that can likely be answered from a knowledge base.

Analyze the user's message carefully. Do not classify a message as 'register_complaint' unless the user clearly states they want to start a new complaint process. If they are just describing a problem (e.g., "My laptop is broken"), it is a 'general_question'.

Here are some examples:
- User Message: "I want to file a complaint about my bill." -> Intent: 'register_complaint'
- User Message: "My laptop is broken, I need to register a grievance." -> Intent: 'register_complaint'
- User Message: "What's the status of my complaint XYZ123?" -> Intent: 'check_status'
- User Message: "What is the return policy for defective items?" -> Intent: 'general_question'
- User Message: "I have an issue with my delivery, it's late." -> Intent: 'general_question'

User Message: '{user_message}'
Intent:"""
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def handle_message(self, session_state, user_message):
        if 'state' not in session_state:
            session_state['state'] = 'initial'

        state = session_state['state']

        if state == 'initial':
            intent = self.get_intent(user_message)
            if 'register_complaint' in intent:
                session_state['state'] = 'awaiting_name'
                session_state['complaint_details'] = {}
                return "I can help with that. What is your name?"
            elif 'check_status' in intent:
                session_state['state'] = 'awaiting_complaint_id'
                return "Sure, what is your complaint ID?"
            else:
                context = self.rag_pipeline.query(user_message)
                prompt = f"""You are a customer support assistant. Use the following piece of context to answer the user's question.
Your answer must be based *only* on the information provided in the context.
If the context does not contain the answer, simply state that you cannot answer the question. Do not try to make up an answer.

Context:
---
{context}
---

Question: {user_message}

Answer:"""
                response = self.llm.invoke(prompt)
                return response.content.strip()

        elif state == 'awaiting_name':
            session_state['complaint_details']['name'] = user_message
            session_state['state'] = 'awaiting_phone'
            return "Thanks. What is your phone number?"

        elif state == 'awaiting_phone':
            session_state['complaint_details']['phone'] = user_message
            session_state['state'] = 'awaiting_email'
            return "Great. What is your email address?"

        elif state == 'awaiting_email':
            session_state['complaint_details']['email'] = user_message
            session_state['state'] = 'awaiting_details'
            return "Got it. Please describe your complaint."

        elif state == 'awaiting_details':
            session_state['complaint_details']['details'] = user_message
            try:
                complaint_id = self.db_manager.create_complaint(
                    session_state['complaint_details']['name'],
                    session_state['complaint_details']['phone'],
                    session_state['complaint_details']['email'],
                    session_state['complaint_details']['details']
                )
                session_state['state'] = 'initial'
                return f"Your complaint has been registered with ID: {complaint_id}"
            except ValueError as e:
                session_state['state'] = 'initial'
                return f"Error: {e}. Please try again."

        elif state == 'awaiting_complaint_id':
            complaint = self.db_manager.get_complaint(user_message)
            session_state['state'] = 'initial'
            if complaint:
                return f"""Here are the details for your complaint:
- **Complaint ID:** {complaint[0]}
- **Name:** {complaint[1]}
- **Phone Number:** {complaint[2]}
- **Email:** {complaint[3]}
- **Details:** {complaint[4]}
- **Status:** {complaint[5]}
- **Registered On:** {complaint[6]}"""
            else:
                return "Invalid complaint ID."
