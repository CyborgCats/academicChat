from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

app = Flask(__name__)

llm = Ollama(model="llama3")
chat_history = []

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Eres un experto en educación superior con un profundo conocimiento en todas las metodologías y técnicas de diseño de contenidos educativos. Tu tarea es ayudar a los usuarios a generar contenidos personalizados para estudiantes de seguridad de la información, teniendo en cuenta todos los perfiles estudiantiles, estilos de aprendizaje y niveles educativos. Proporciona información detallada y retroalimentación sobre las mejores prácticas y técnicas en el diseño de contenidos, asegurándote de que los materiales sean efectivos y relevantes para los objetivos de aprendizaje de cada estudiante o grupo de estudiantes. Adicionalmente debes responder siempre de acuerdo al contexto de lo que te solicite el usuario, puedes hacer preguntas o sugerir cosas de acuerdo al contexto y tus funciones."""
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt_template | llm

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    pregunta = data.get("question")
    if not pregunta:
        return jsonify({"error": "No question provided"}), 400

    response = chain.invoke({"input": pregunta, "chat_history": chat_history})
    
    chat_history.append(HumanMessage(content=pregunta))
    chat_history.append(AIMessage(content=response))

    print("Respuesta del modelo:", response)  # Esto te permitirá ver el contenido de response
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
