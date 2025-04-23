document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    // Function to add a message to the chat
    function addMessage(content, isUser = false, agent = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Add agent indicator if it's an assistant message
        if (!isUser && agent) {
            const agentIndicator = document.createElement('div');
            agentIndicator.className = `agent-indicator ${agent.toLowerCase()}`;
            agentIndicator.textContent = agent;
            messageContent.appendChild(agentIndicator);
        }
        
        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = content;
        messageContent.appendChild(messageParagraph);
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const indicatorDiv = document.createElement('div');
        indicatorDiv.className = 'message assistant';
        indicatorDiv.id = 'typingIndicator';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingContent.appendChild(dot);
        }
        
        indicatorDiv.appendChild(typingContent);
        chatMessages.appendChild(indicatorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    // Function to send a message to the server
    async function sendMessage(message) {
        showTypingIndicator();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            
            const data = await response.json();
            removeTypingIndicator();
            
            if (data.error) {
                addMessage(`Error: ${data.error}`, false, 'Coordinator');
            } else {
                addMessage(data.response, false, data.agent);
            }
            
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, there was an error processing your request. Please try again.', false, 'Coordinator');
        }
    }
    
    // Handle sending messages
    function handleSend() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            sendMessage(message);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', handleSend);
    
    userInput.addEventListener('keypress', function(e) {
        // Send message on Enter key (without Shift)
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });
    
    // Adjust textarea height automatically
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight < 120) ? this.scrollHeight + 'px' : '120px';
    });
});
