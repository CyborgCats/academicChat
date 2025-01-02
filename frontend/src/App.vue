<template>
  <div id="app">
    <h1>Chat con AI</h1>
    <div v-for="(message, index) in chatHistory" :key="index" class="message">
      <p><strong>{{ message.sender }}:</strong> {{ message.text }}</p>
    </div>
    <input v-model="question" @keyup.enter="sendQuestion" placeholder="Escribe tu pregunta..." />
    <button @click="sendQuestion">Enviar</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      question: '',
      chatHistory: [],
    };
  },
  methods: {
    async sendQuestion() {
      if (this.question.trim() === '') return;

      this.chatHistory.push({ sender: 'Yo', text: this.question });
      try {
        const response = await axios.post('http://localhost:5000/chat', {
          question: this.question,
        });

        this.chatHistory.push({ sender: 'AI', text: response.data.response });
        this.question = '';
      } catch (error) {
        console.error('Error al comunicarse con la API:', error);
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

.message {
  margin: 10px 0;
}
</style>
