import gradio as gr
import requests
import os
# Define the API endpoint
API_URL = "https://us-central1-gen-ai-wit-rag.cloudfunctions.net/bot_mongo-2"

# Define functions to interact with the API
def register_user_interface(employee_code, password):
    payload = {
        'action': 'register',
        'employee_code': employee_code,
        'password': password
    }
    response = requests.post(API_URL, json=payload)
    result = response.json()
    return result['message']

def login_user_interface(employee_code, password):
    payload = {
        'action': 'login',
        'employee_code': employee_code,
        'password': password
    }
    response = requests.post(API_URL, json=payload)
    result = response.json()
    if result['status'] == 'success':
        return result['message'], {'employee_code': employee_code, 'password': password}
    else:
        return result['message'], None

def chat_interface(user_input,history,user_credentials):
    if user_credentials is None:
        return "Please log in first."
    
    employee_code = user_credentials['employee_code']
    password = user_credentials['password']
    
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

def clear_chat_history_interface(user_credentials):
    if user_credentials is None:
        return "Please log in first."
    
    employee_code = user_credentials['employee_code']
    password = user_credentials['password']
    
    payload = {
        'action': 'clear_chat_history',
        'employee_code': employee_code,
        'password': password
    }
    response = requests.post(API_URL, json=payload)
    result = response.json()
    return result['message']

# Gradio interface
with gr.Blocks() as demo:
    user_credentials = gr.State(None)

    with gr.Tab("Register"):
        with gr.Row():
            employee_code_reg = gr.Textbox(label="Employee Code")
            password_reg = gr.Textbox(label="Password", type="password")
        register_btn = gr.Button("Register")
        register_output = gr.Textbox(label="Output")
        
        register_btn.click(register_user_interface, inputs=[employee_code_reg, password_reg], outputs=register_output)

    with gr.Tab("Login"):
        with gr.Row():
            employee_code_login = gr.Textbox(label="Employee Code")
            password_login = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_output = gr.Textbox(label="Output")
        
        login_btn.click(
            login_user_interface, 
            inputs=[employee_code_login, password_login], 
            outputs=[login_output, user_credentials]
        )
        
    with gr.Tab("Chat"):
        gr.ChatInterface(fn=chat_interface, additional_inputs=[user_credentials], title="Chat Bot")
    
    with gr.Tab("Clear Chat History"):
        clear_history_btn = gr.Button("Clear History")
        clear_history_output = gr.Textbox(label="Output")

        clear_history_btn.click(clear_chat_history_interface, inputs=[user_credentials], outputs=clear_history_output)

# Get the port from the environment variable
port = int(os.environ.get('PORT', 7860))

# Launch the Gradio interface
demo.launch(server_name="0.0.0.0", server_port=port)
