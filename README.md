 A chatbot with langgraph - ReAct agent 
# 🤖 ReAct-Agent Chatbot

A modular, reasoning-augmented chatbot framework that combines Retrieval-Augmented Generation (RAG), online search, and advanced memory for dynamic, context-aware conversations. Built with Python, Gradio, and LangGraph.

---

## ✨ Features

- **Reasoning Node**: Decides the best tool (RAG, online search, or direct reply) for each user query.
- **RAG Tool**: Retrieves relevant knowledge from your own PDF/document database using vector search and Gemini LLM.
- **Tavily Tool**: Performs real-time web search for up-to-date answers.
- **Chat Memory**: Remembers recent conversation history for contextually rich responses.
- **MongoDB Integration**: Stores chat history and document embeddings.
- **Modern UI**: Clean, interactive chat interface powered by Gradio.

---



## 🚀 Quickstart

1. **Clone the repo**
	```bash
	git clone https://github.com/arshaimran/ReAct-agent-chatbot.git
	cd ReAct-agent-chatbot
	```
2. **Install dependencies**
	```bash
	pip install -r requirements.txt
	```
3. **Set up environment variables**
	- Copy `.env.example` to `.env` and fill in:
	  - `GEMINI_API_KEY`, `GEMINI_URL`, `MONGO_URI`, `TAVILY_API_KEY`
4. **Run the app**
	```bash
	cd agent/src
	python ui.py
	```
5. **Open in browser**
	- Visit [http://localhost:7860](http://localhost:7860)

---

## 🛠️ Project Structure

```
agent/
  src/
	 graph.py           # LangGraph workflow
	 ui.py              # Gradio UI
	 nodes/
		reasoning_node.py  # Tool selection logic
		tool_nodes.py      # RAG & Tavily tool nodes
	 utils/
		dbhistory.py     # MongoDB chat history
		logger.py        # Logging
		memory.py        # Chat memory prompt
README.md
```

---

## 📚 Tech Stack
- Python, Gradio, LangGraph
- Gemini LLM, Tavily API
- MongoDB, Sentence Transformers

---

## 🤝 Contributing
Pull requests and issues are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
MIT License © 2025 arshaimran
