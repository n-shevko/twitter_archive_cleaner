Vue.createApp({
  data() {
    return {
      messages: window.messages,
      activeConversation: 0,
      search: ''
    }
  },
  computed: {
    filteredMessages() {
      let messages = this.messages[this.activeConversation].messages
      return messages.filter(item => item.text.toLowerCase().includes(this.search.toLowerCase()));
    }
  },
  methods: {
    formatDt(dt) {
      const date = new Date(dt);
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
        timeZone: 'America/New_York'
      };
      return date.toLocaleString('en-US', options);
    },
    switchConverstation(idx) {
      this.activeConversation = idx
    }
  }
}).mount('#app')