import gradio as gr
import requests
import os

# Define the API endpoint
API_URL = "https://us-central1-gen-ai-wit-rag.cloudfunctions.net/bot_mongo-1"

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
        chat_url = f"https://huggingface.co/spaces/YOUR_USERNAME/YOUR_CHAT_SPACE?employee_code={employee_code}&password={password}"
        return result['message'], chat_url
    else:
        return result['message'], None

# Gradio interface for Registration and Login
with gr.Blocks() as login_demo:
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
        chat_url = gr.Textbox(label="Chat URL", visible=False)
        
        login_btn.click(
            login_user_interface, 
            inputs=[employee_code_login, password_login], 
            outputs=[login_output, chat_url]
        )

# Get the port from the environment variable
port = int(os.environ.get('PORT', 7860))

# Launch the Gradio interface
login_demo.launch(server_port=port)
