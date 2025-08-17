🤖 Advanced Offline Chatbot
Website Link: https://abhirambuilds.github.io/mini-projects-2025/project-1-todo-list/

A comprehensive offline chatbot application built with HTML, CSS, and JavaScript, featuring an intelligent knowledge base, fuzzy matching, math solving, and a modern chat UI. This project demonstrates how AI-like assistants can be simulated without relying on external APIs or internet access.

✨ Features
💡 Core Functionalities

Knowledge Base: Loads 40,000+ Q&A pairs from a local JSON file

Fuzzy Matching: Uses the Levenshtein distance algorithm for intelligent matching of similar questions

Math Solver: Handles basic arithmetic & expressions (e.g., 23*4+5)

Time & Date: Responds with real-time system time and date

Conversation Memory: Saves chat history in localStorage

Export Chat: Download chat history as a JSON file

🎨 User Interface

Modern Chat Layout: Speech bubble design

Typing Animation: Shows chatbot typing before responding

Responsive Design: Optimized for mobile and desktop

Dark/Light Theme Ready: Easily customizable

🔒 Offline-First

No internet required

No API keys

All data stored locally (JSON + browser localStorage)

🛠 Technical Implementation

Frontend: HTML5, CSS3, JavaScript (ES6+)

Algorithms: Levenshtein distance (fuzzy matching), expression parsing

Data Storage: JSON file for Q&A, browser localStorage for session persistence

Performance: Optimized string matching and efficient dataset loading

📁 Project Structure
project-6-offline-chatbot/
├── index.html          # Main UI file
├── style.css           # Chat UI styling
├── script.js           # Chatbot logic
├── data/
│   └── knowledge.json  # 40,000+ Q&A pairs
├── assets/             # Icons, optional images
└── README.md           # Documentation

🚀 Getting Started
Prerequisites

Modern web browser (Chrome, Firefox, Edge, Safari)

Steps to Run

Clone or download the repository

git clone <repo-url>
cd project-6-offline-chatbot


Open index.html in your browser

Start chatting with the offline AI assistant

🎯 Usage Guide

Ask Questions: Type questions like "What is Python?" or "Who is Albert Einstein?"

Do Math: Try "45 + 72" or "(105) - 12"*

Check Time: Ask "What’s the time?" or "Tell me today’s date"

Export Chat: Click the download button to save your conversation

🔧 Customization
Adding Knowledge

Add more Q&A pairs inside data/knowledge.json:

{
  "question": "What is AI?",
  "answer": "AI stands for Artificial Intelligence, the simulation of human intelligence in machines."
}

Changing Theme

Modify style.css to switch between light/dark or update chat bubble colors.

Adjusting Matching Sensitivity

Tune Levenshtein threshold inside script.js to make answers stricter or more flexible.

📊 Learning Outcomes

JavaScript algorithms (Levenshtein distance, expression parsing)

Handling large datasets in the browser

Building responsive and animated chat UIs

Working with localStorage for persistence

Optimizing offline-first applications

🐛 Troubleshooting

App not loading answers → Check that knowledge.json is in the correct path

Slow matching → Reduce dataset size or adjust algorithm threshold

Math errors → Ensure input is a valid expression

🚀 Future Enhancements

🎙 Voice Input/Output (speech recognition & TTS)

🌍 Multi-language Support

🧠 ML/NLP integration for smarter responses

☁ Cloud Sync for storing history across devices

🎨 Dark Mode toggle

📄 License

This project is open source and available under the MIT License.

🙏 Acknowledgments

Levenshtein Distance Algorithm for fuzzy string matching

Math.js inspiration for math parsing ideas

Modern UI patterns from chat apps (WhatsApp, Messenger)

