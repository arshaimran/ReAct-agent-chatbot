import gradio as gr
from graph import app
import uuid

def respond(message, history, session_id):
    print("Session ID:", session_id)
    # Run through LangGraph
    initial_state = {
        "history": [],
        "user_input": message,
        "result": "",
        "session_id": session_id
    }
    output = app.invoke(initial_state)
    bot_reply = output["result"]

    # Update history (messages format)
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": bot_reply}
    ]
    return history, history, session_id

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat",type="messages")
    msg = gr.Textbox(placeholder="Ask me anything", label="Your messsage")
    clear = gr.Button("Clear")
    session_id_state = gr.State(value=str(uuid.uuid4()))

    msg.submit(respond, [msg, chatbot, session_id_state], [chatbot, chatbot, session_id_state])
    clear.click(lambda: [], None, chatbot)

demo.launch()
