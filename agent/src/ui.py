import gradio as gr
from graph import app

def respond(message, history):
    # Run through LangGraph
    initial_state = {
        "history": [],
        "user_input": message,
        "result": ""
    }
    output = app.invoke(initial_state)
    bot_reply = output["result"]

    # Update history (messages format)
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": bot_reply}
    ]
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [chatbot, chatbot])
    clear.click(lambda: [], None, chatbot)

demo.launch()
