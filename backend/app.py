from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

app = Flask(__name__)
CORS(app)  # Esto permite las solicitudes desde tu frontend Vue.js

llm = Ollama(model="llama3")
chat_history = []

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Eres un experto en educación superior con un profundo conocimiento en todas las metodologías y técnicas de diseño de contenidos educativos..."""
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt_template | llm

@app.route('/', methods=['GET'])
def home():
    return "El servidor está corriendo correctamente", 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    pregunta = data.get("question")
    if not pregunta:
        return jsonify({"error": "No question provided"}), 400

    response = chain.invoke({"input": pregunta, "chat_history": chat_history})
    chat_history.append(HumanMessage(content=pregunta))
    chat_history.append(AIMessage(content=response))

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
