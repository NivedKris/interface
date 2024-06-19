import gradio as gr
import requests
import os
# Define the API endpoint
API_URL = "https://us-central1-gen-ai-wit-rag.cloudfunctions.net/bot_mongo-2"

   


def chat_interface(user_input,history):
    if user_credentials is None:
        return "Please log in first."
    
    employee_code = '1'
    password = '1'
    
    payload = {
        'action': 'chat',
        'employee_code': employee_code,
        'password': password,
        'input': user_input
    }
    response = requests.post(API_URL, json=payload)
    result = response.json()
    if result['status'] == 'success':
        return result['answer']
    else:
        return result['message']



chatbot=gr.ChatInterface(fn=chat_interface,title="PROTOTYPE")
    


# Get the port from the environment variable
port = int(os.environ.get('PORT', 7860))

# Launch the Gradio interface
chatbot.launch(server_name="0.0.0.0", server_port=port)
