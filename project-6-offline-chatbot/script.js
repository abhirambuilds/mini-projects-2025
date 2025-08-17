/**
 * Advanced Offline Chatbot
 * Features: Fuzzy matching, Math calculations, Modern UI, Knowledge base search
 * Author: Developer
 * Version: 2.0
 */

class AdvancedOfflineChatbot {
    constructor() {
        // Core properties
        this.knowledgeBase = {};
        this.conversationHistory = [];
        this.isTyping = false;
        this.typingTimeout = null;
        
        // DOM elements
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        // Initialize the chatbot
        this.initializeChatbot();
        this.setupEventListeners();
        this.loadConversationHistory();
    }

    /**
     * Initialize the chatbot by loading knowledge base
     */
    async initializeChatbot() {
        try {
            console.log('🚀 Initializing Advanced Offline Chatbot...');
            
            // Show loading overlay
            this.showLoadingOverlay();
            
            // Load knowledge base from knowledge_base2.json
            await this.loadKnowledgeBase();
            
            // Hide loading overlay
            this.hideLoadingOverlay();
            
            // Display welcome message
            this.displayWelcomeMessage();
            
            // Update knowledge base count
            this.updateKnowledgeCount();
            
            console.log('🎉 Chatbot initialization complete!');
            
        } catch (error) {
            console.error('💥 Error initializing chatbot:', error);
            this.hideLoadingOverlay();
            this.displayErrorMessage('Failed to load knowledge base. Please refresh the page.');
        }
    }

    /**
     * Load comprehensive knowledge base from knowledge_base2.json
     */
    async loadKnowledgeBase() {
        try {
            console.log('🔄 Loading knowledge base...');
            
            // Try to load the large dataset directly from knowledge_base2.json
            console.log('🔄 Attempting to fetch knowledge_base2.json...');
            const response = await fetch('knowledge_base2.json');
            
            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);
            console.log('Response headers:', response.headers);
            
            if (response.ok) {
                const largeDataset = await response.json();
                
                console.log(`📊 Dataset loaded: ${largeDataset.length} items`);
                console.log('First few items:', largeDataset.slice(0, 3));
                
                // Transform the large dataset into our format
                const transformedData = largeDataset.map(item => ({
                    question: item.question.toLowerCase().trim(),
                    answer: item.answer,
                    category: 'comprehensive'
                }));
                
                // Set the knowledge base
                this.knowledgeBase = {
                    comprehensive: transformedData,
                    greetings: this.getDefaultGreetings(),
                    personal: this.getDefaultPersonal(),
                    fun: this.getDefaultFun()
                };
                
                console.log(`✅ Successfully loaded knowledge base with ${transformedData.length} Q&A pairs`);
                console.log('Knowledge base structure:', Object.keys(this.knowledgeBase));
                
            } else {
                throw new Error(`Failed to load knowledge_base2.json: ${response.status} ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Error loading knowledge base:', error);
            console.warn('⚠️ Using fallback knowledge base...');
            
            // Fallback to basic knowledge base
            this.knowledgeBase = {
                comprehensive: this.getFallbackComprehensive(),
                greetings: this.getDefaultGreetings(),
                personal: this.getDefaultPersonal(),
                fun: this.getDefaultFun()
            };
            
            console.log('🔄 Fallback knowledge base loaded');
            console.log('Fallback knowledge base size:', this.knowledgeBase.comprehensive.length);
        }
    }

    /**
     * Get default greetings for fallback
     */
    getDefaultGreetings() {
        return [
            { question: "hi", answer: "Hello! 👋 How can I help you today?", category: "greetings" },
            { question: "hello", answer: "Hi there! 😊 Nice to meet you! How may I assist you?", category: "greetings" },
            { question: "hey", answer: "Hey! 👋 What's on your mind? I'm here to help!", category: "greetings" },
            { question: "good morning", answer: "Good morning! 🌅 Hope you're having a wonderful start to your day. How can I help?", category: "greetings" },
            { question: "good night", answer: "Good night! 🌙 Sleep well and have sweet dreams. Feel free to chat with me anytime!", category: "greetings" }
        ];
    }

    /**
     * Get default personal questions for fallback
     */
    getDefaultPersonal() {
        return [
            { question: "what's your name?", answer: "I'm Advanced Chatbot, your friendly offline AI companion! 🤖 Nice to meet you!", category: "personal" },
            { question: "who created you?", answer: "I was created as an advanced learning project to demonstrate web development skills, AI capabilities, and natural language processing. I'm built with love for coding! 💻", category: "personal" },
            { question: "how old are you?", answer: "I'm a relatively new AI chatbot, created as a learning project. While I don't have a physical age, I'm designed to help and learn from our conversations! 📚", category: "personal" }
        ];
    }

    /**
     * Get default fun content for fallback
     */
    getDefaultFun() {
        return [
            { question: "tell me a joke", answer: "Why don't scientists trust atoms? Because they make up everything! 😄 Here's another: What do you call a fake noodle? An impasta! 🍝", category: "fun" },
            { question: "tell me a riddle", answer: "Here's a fun riddle: What has keys, but no locks; space, but no room; and you can enter, but not go in? 🤔 The answer is a computer keyboard! ⌨️", category: "fun" }
        ];
    }

    /**
     * Get fallback comprehensive data
     */
    getFallbackComprehensive() {
        return [
            { question: "what is the boiling point of water?", answer: "The boiling point of water is 100°C at standard pressure.", category: "comprehensive" },
            { question: "who developed the theory of relativity?", answer: "The theory of relativity was developed by Albert Einstein.", category: "comprehensive" },
            { question: "what is the capital of france?", answer: "The capital of France is Paris.", category: "comprehensive" },
            { question: "what is dna?", answer: "DNA (deoxyribonucleic acid) is a molecule that carries genetic information and instructions for the development and functioning of living organisms.", category: "comprehensive" },
            { question: "what is the current time?", answer: this.getCurrentTime(), category: "comprehensive" },
            { question: "what time is it?", answer: this.getCurrentTime(), category: "comprehensive" },
            { question: "what is time?", answer: this.getCurrentTime(), category: "comprehensive" },
            { question: "tell me the time", answer: this.getCurrentTime(), category: "comprehensive" },
            { question: "what day is today?", answer: this.getCurrentDate(), category: "comprehensive" },
            { question: "what is today's date?", answer: this.getCurrentDate(), category: "comprehensive" },
            { question: "what date is it today?", answer: this.getCurrentDate(), category: "comprehensive" }
        ];
    }

    /**
     * Setup event listeners for user interactions
     */
    setupEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.handleUserInput());
        
        // Enter key press
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleUserInput();
            }
        });

        // Quick action buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.getAttribute('data-query');
                this.userInput.value = query;
                this.handleUserInput();
            });
        });

        // Control buttons
        document.getElementById('testBtn').addEventListener('click', () => this.testKnowledgeBase());
        document.getElementById('clearChatBtn').addEventListener('click', () => this.clearChat());
        document.getElementById('helpBtn').addEventListener('click', () => this.showHelpModal());
        document.getElementById('aboutBtn').addEventListener('click', () => this.showAboutModal());
        document.getElementById('exportChatBtn').addEventListener('click', () => this.exportChat());
        
        // Modal close buttons
        document.getElementById('closeHelpBtn').addEventListener('click', () => this.hideModal('helpModal'));
        document.getElementById('closeAboutBtn').addEventListener('click', () => this.hideModal('aboutModal'));
        
        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });

        // Voice button (placeholder for future implementation)
        document.getElementById('voiceBtn').addEventListener('click', () => {
            this.displayBotMessage("🎤 Voice input feature coming soon! For now, please type your message.");
        });

        // Emoji button (placeholder for future implementation)
        document.getElementById('emojiBtn').addEventListener('click', () => {
            this.displayBotMessage("😊 Emoji picker feature coming soon! You can type emojis directly.");
        });
    }

    /**
     * Handle user input and generate response
     */
    handleUserInput() {
        const userMessage = this.userInput.value.trim();
        if (!userMessage) return;

        // Add user message to chat
        this.addUserMessage(userMessage);
        
        // Clear input
        this.userInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Process message and generate response
        setTimeout(() => {
            this.hideTypingIndicator();
            const response = this.generateResponse(userMessage);
            this.displayBotMessage(response);
        }, 1000 + Math.random() * 1000); // Random delay for natural feel
    }

    /**
     * Generate appropriate response based on user input
     */
    generateResponse(userMessage) {
        const message = userMessage.toLowerCase().trim();
        console.log(`🤖 Generating response for: "${userMessage}"`);
        
        // Check if it's a math expression
        if (this.isMathExpression(message)) {
            console.log(`🧮 Detected math expression: "${message}"`);
            return this.solveMathExpression(message);
        }
        
        // Check if it's a time-related question
        if (this.isTimeQuestion(message)) {
            console.log(`⏰ Detected time question: "${message}"`);
            return this.getCurrentTime();
        }
        
        // Check if it's a date-related question
        if (this.isDateQuestion(message)) {
            console.log(`📅 Detected date question: "${message}"`);
            return this.getCurrentDate();
        }
        
        // Search knowledge base for best match
        console.log(`🔍 Searching knowledge base for: "${message}"`);
        const bestMatch = this.findBestMatch(message);
        
        if (bestMatch) {
            console.log(`✅ Returning matched answer: "${bestMatch.answer.substring(0, 50)}..."`);
            return bestMatch.answer;
        }
        
        // Fallback response
        console.log(`❌ No match found, using fallback response`);
        return this.getFallbackResponse(message);
    }

    /**
     * Check if input is a math expression
     */
    isMathExpression(text) {
        // Remove common words and check for mathematical operators
        const cleanText = text.replace(/what is|calculate|solve|compute|equal|equals|answer|result/gi, '').trim();
        const mathPattern = /^[\d\s\+\-\*\/\(\)\.\^%]+$/;
        return mathPattern.test(cleanText) && /[\+\-\*\/\^%]/.test(cleanText);
    }
    
    /**
     * Check if input is a time-related question
     */
    isTimeQuestion(text) {
        const timePatterns = [
            /what.*time/i,
            /what time/i,
            /current time/i,
            /time now/i,
            /tell me.*time/i,
            /what.*o'clock/i,
            /what.*hour/i
        ];
        return timePatterns.some(pattern => pattern.test(text));
    }
    
    /**
     * Check if input is a date-related question
     */
    isDateQuestion(text) {
        const datePatterns = [
            /what.*date/i,
            /what date/i,
            /current date/i,
            /today.*date/i,
            /what day.*today/i,
            /tell me.*date/i,
            /what.*day/i
        ];
        return datePatterns.some(pattern => pattern.test(text));
    }

    /**
     * Solve basic math expressions
     */
    solveMathExpression(expression) {
        try {
            // Clean the expression
            let cleanExpr = expression.replace(/what is|calculate|solve|compute|equal|equals|answer|result/gi, '').trim();
            
            // Handle common mathematical operations
            cleanExpr = cleanExpr.replace(/\^/g, '**'); // Convert ^ to **
            cleanExpr = cleanExpr.replace(/×/g, '*'); // Convert × to *
            cleanExpr = cleanExpr.replace(/÷/g, '/'); // Convert ÷ to /
            
            // Evaluate the expression
            const result = eval(cleanExpr);
            
            // Check if result is valid
            if (isFinite(result) && !isNaN(result)) {
                return `🧮 The answer is: ${result}`;
            } else {
                throw new Error('Invalid result');
            }
        } catch (error) {
            console.error('Math calculation error:', error);
            return "❌ I couldn't solve that math expression. Please make sure it's a valid mathematical operation (e.g., '2 + 3', '10 * 5', '100 / 4').";
        }
    }

    /**
     * Find best match using fuzzy matching algorithm
     */
    findBestMatch(query, threshold = 0.6) {
        console.log(`🔍 Searching for: "${query}"`);
        console.log(`🔍 Knowledge base categories:`, Object.keys(this.knowledgeBase));
        
        let bestMatch = null;
        let bestScore = 0;
        
        // Search through all categories
        Object.values(this.knowledgeBase).forEach(category => {
            if (Array.isArray(category)) {
                console.log(`🔍 Searching category with ${category.length} items`);
                category.forEach(item => {
                    const score = this.calculateSimilarity(query, item.question);
                    if (score > bestScore && score >= threshold) {
                        bestScore = score;
                        bestMatch = { ...item, confidence: score };
                        console.log(`🔍 New best match: "${item.question}" with score ${score}`);
                    }
                });
            }
        });
        
        if (bestMatch) {
            console.log(`✅ Found match: "${bestMatch.question}" with confidence ${bestMatch.confidence}`);
        } else {
            console.log(`❌ No match found above threshold ${threshold}`);
        }
        
        return bestMatch;
    }

    /**
     * Calculate similarity between two strings using Levenshtein distance
     */
    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1.0;
        
        // Calculate Levenshtein distance
        const distance = this.levenshteinDistance(longer, shorter);
        const similarity = (longer.length - distance) / longer.length;
        
        return similarity;
    }

    /**
     * Calculate Levenshtein distance between two strings
     */
    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }

    /**
     * Get fallback response when no match is found
     */
    getFallbackResponse(query) {
        const fallbackResponses = [
            "🤔 I don't know that yet, but I can help you with many other topics!",
            "❓ That's an interesting question, but it's not in my knowledge base yet.",
            "💭 I'm not sure about that, but I'd be happy to help with something else!",
            "🔍 I couldn't find information about that in my knowledge base.",
            "📚 That's beyond my current knowledge, but I'm always learning!"
        ];
        
        // Check if it's a greeting-like message
        if (/^(hi|hello|hey|good|morning|afternoon|evening|night)/.test(query)) {
            return "Hello! 👋 How can I help you today?";
        }
        
        // Check if it's a farewell
        if (/^(bye|goodbye|see you|farewell|take care)/.test(query)) {
            return "Goodbye! 👋 Have a wonderful day! Come back anytime!";
        }
        
        // Check if it's a thank you
        if (/^(thank|thanks|thx|appreciate)/.test(query)) {
            return "You're welcome! 😊 I'm happy to help!";
        }
        
        // Random fallback response
        return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
    }

    /**
     * Add user message to chat
     */
    addUserMessage(message) {
        const messageElement = this.createMessageElement(message, 'user');
        this.chatMessages.appendChild(messageElement);
        
        // Save to conversation history
        this.conversationHistory.push({
            type: 'user',
            message: message,
            timestamp: new Date().toISOString()
        });
        
        // Save conversation
        this.saveConversationHistory();
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    /**
     * Display bot message
     */
    displayBotMessage(message) {
        const messageElement = this.createMessageElement(message, 'bot');
        this.chatMessages.appendChild(messageElement);
        
        // Save to conversation history
        this.conversationHistory.push({
            type: 'bot',
            message: message,
            timestamp: new Date().toISOString()
        });
        
        // Save conversation
        this.saveConversationHistory();
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    /**
     * Create message element
     */
    createMessageElement(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '👤' : '🤖';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = message;
        
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        messageDiv.appendChild(time);
        
        return messageDiv;
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typingIndicator';
        
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    /**
     * Display welcome message
     */
    displayWelcomeMessage() {
        const welcomeMessage = `Hello! I'm your Advanced Offline Chatbot! 🤖

I'm powered by a comprehensive knowledge base covering:
• Science & Technology 🔬
• History & Geography 🌍
• Mathematics & Logic 🧮
• General Knowledge 📚
• Fun & Entertainment 😄

I can also solve basic math calculations and understand variations of questions using fuzzy matching.

What would you like to know?`;
        
        this.displayBotMessage(welcomeMessage);
    }

    /**
     * Display error message
     */
    displayErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message bot error';
        errorDiv.innerHTML = `
            <div class="message-avatar">⚠️</div>
            <div class="message-content">${message}</div>
            <div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
        `;
        
        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();
    }

    /**
     * Scroll chat to bottom
     */
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    /**
     * Clear chat history
     */
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.chatMessages.innerHTML = '';
            this.conversationHistory = [];
            this.saveConversationHistory();
            this.displayWelcomeMessage();
        }
    }

    /**
     * Show help modal
     */
    showHelpModal() {
        document.getElementById('helpModal').style.display = 'block';
    }

    /**
     * Show about modal
     */
    showAboutModal() {
        document.getElementById('aboutModal').style.display = 'block';
    }

    /**
     * Hide modal
     */
    hideModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    /**
     * Export chat history
     */
    exportChat() {
        const chatData = {
            exportDate: new Date().toISOString(),
            conversation: this.conversationHistory
        };
        
        const dataStr = JSON.stringify(chatData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `chatbot-conversation-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    }

    /**
     * Update knowledge base count
     */
    updateKnowledgeCount() {
        // No longer displaying detailed counts
        console.log('📚 Knowledge base loaded successfully');
    }
    
    /**
     * Show loading overlay
     */
    showLoadingOverlay() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'flex';
        }
    }

    /**
     * Hide loading overlay
     */
    hideLoadingOverlay() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'none';
        }
    }

    /**
     * Save conversation history to localStorage
     */
    saveConversationHistory() {
        try {
            localStorage.setItem('chatbotConversation', JSON.stringify(this.conversationHistory));
        } catch (error) {
            console.warn('Could not save conversation to localStorage:', error);
        }
    }

    /**
     * Load conversation history from localStorage
     */
    loadConversationHistory() {
        try {
            const savedConversation = localStorage.getItem('chatbotConversation');
            
            if (savedConversation) {
                this.conversationHistory = JSON.parse(savedConversation);
                
                // Display conversation history
                this.displayConversationHistory();
            }
        } catch (error) {
            console.warn('Could not load conversation from localStorage:', error);
        }
    }

    /**
     * Display conversation history
     */
    displayConversationHistory() {
        if (this.conversationHistory.length === 0) return;
        
        // Clear current messages
        this.chatMessages.innerHTML = '';
        
        // Display all messages
        this.conversationHistory.forEach(item => {
            if (item.type === 'user') {
                this.addUserMessage(item.message);
            } else {
                this.displayBotMessage(item.message);
            }
        });
        
        // Scroll to bottom
        this.scrollToBottom();
    }

    /**
     * Test knowledge base status
     */
    testKnowledgeBase() {
        console.log('🧪 Testing Knowledge Base...');
        console.log('Knowledge base structure:', this.knowledgeBase);
        
        Object.entries(this.knowledgeBase).forEach(([category, data]) => {
            if (Array.isArray(data)) {
                console.log(`📊 ${category}: ${data.length} items`);
                if (data.length > 0) {
                    console.log(`   Sample: "${data[0].question}" -> "${data[0].answer.substring(0, 50)}..."`);
                }
            }
        });
        
        // Test a simple search
        const testQuery = "what is time";
        console.log(`🧪 Testing search for: "${testQuery}"`);
        const result = this.findBestMatch(testQuery);
        
        if (result) {
            this.displayBotMessage(`✅ Knowledge Base Test: Found "${result.question}" with confidence ${result.confidence.toFixed(2)}`);
        } else {
            this.displayBotMessage(`❌ Knowledge Base Test: No match found for "${testQuery}"`);
        }
    }

    /**
     * Get current time
     */
    getCurrentTime() {
        const now = new Date();
        return `The current time is ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }

    /**
     * Get current date
     */
    getCurrentDate() {
        const now = new Date();
        return `Today's date is ${now.toLocaleDateString()}`;
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing Advanced Offline Chatbot...');
    window.chatbot = new AdvancedOfflineChatbot();
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedOfflineChatbot;
}
