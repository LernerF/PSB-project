<template>
  <div class="chat-container">
    <h1>RAG Чат</h1>
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender]">
        <div class="message-content">{{ msg.text }}</div>
        <div class="message-time">{{ msg.time }}</div>
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="inputMessage"
        @keyup.enter="sendMessage"
        placeholder="Введите ваше сообщение..."
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="!inputMessage || isLoading">
        {{ isLoading ? 'Отправка...' : 'Отправить' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputMessage: '',
      messages: [],
      isLoading: false,
      userId: null
    }
  },
  async created() {
    // Инициализация чата с получением user_id
    const response = await fetch('/api/init_chat')
    const data = await response.json()
    this.userId = data.user_id
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim()) return

      const userMessage = this.inputMessage
      this.addMessage(userMessage, 'user')
      this.inputMessage = ''
      this.isLoading = true

      try {
        const response = await fetch('/api/send_message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: userMessage,
            user_id: this.userId
          })
        })

        if (!response.ok) {
          throw new Error(await response.text())
        }

        const data = await response.json()
        this.addMessage(data.text, 'bot')
      } catch (error) {
        this.addMessage('Произошла ошибка при отправке сообщения.', 'bot')
        console.error('Ошибка:', error)
      } finally {
        this.isLoading = false
      }
    },
    addMessage(text, sender) {
      const now = new Date()
      const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      this.messages.push({ text, sender, time })
      
      // Прокрутка к последнему сообщению
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        container.scrollTop = container.scrollHeight
      })
    }
  }
}
</script>

<style>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  height: 90vh;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.message {
  margin-bottom: 15px;
  max-width: 80%;
}

.message.user {
  margin-left: auto;
  text-align: right;
}

.message.bot {
  margin-right: auto;
  text-align: left;
}

.message-content {
  padding: 8px 12px;
  border-radius: 15px;
  display: inline-block;
}

.user .message-content {
  background-color: #007bff;
  color: white;
}

.bot .message-content {
  background-color: #e9ecef;
  color: black;
}

.message-time {
  font-size: 0.8em;
  color: #666;
  margin-top: 4px;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.chat-input button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.chat-input button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>