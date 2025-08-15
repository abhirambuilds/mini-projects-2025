📝 Markdown Blog Site (Python Flask)

A lightweight local Markdown blogging platform built with Python Flask, featuring user authentication, role-based access control, and a modern, responsive interface.

✨ Features
👥 User Authentication

Register, log in, and manage accounts securely

Password hashing & session management

🔑 Role-Based Access

Regular Users: Create, edit, and delete their own posts

Admins: Manage all posts and users, access admin dashboard

📰 Post Management

Create, edit, delete Markdown posts

Local storage as .md files

Markdown → HTML rendering for display

🔍 Search & Interaction

Search posts by title

Like/unlike posts (one like per user)

Mobile-friendly responsive UI (Bootstrap)

📦 Requirements

Python 3.7+

Flask

Flask-SQLAlchemy

Markdown

Werkzeug

Install dependencies:

pip install -r requirements.txt

🚀 Getting Started

Clone the repository

git clone <repo_url>
cd markdown-blog


Install dependencies

pip install -r requirements.txt


Run the app

python app.py


Open in browser

http://localhost:5000

🔑 Default Admin Account

Username: admin

Password: admin123
(Created automatically on first run)

👤 User Roles
Regular Users

✅ Create & view posts
✅ Search posts
✅ Manage profile & password
✅ Delete their own posts

❌ Edit other users’ posts
❌ Delete other users’ posts

Administrators

✅ All regular user privileges
✅ Edit/delete any post
✅ View all registered users
✅ Grant/revoke admin privileges
✅ Delete user accounts
✅ Access admin dashboard

📂 File Structure
project-4-markdown-blog/
├── app.py
├── blog.db
├── posts/
│   ├── example-post.md
│   ├── encyclopedia.md
│   └── flask-web-development.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── post.html
│   ├── create.html
│   ├── edit.html
│   ├── search.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── change_password.html
├── static/
│   └── style.css
├── requirements.txt
└── README.md

🛡 Security Features

Password hashing (Werkzeug)

Session-based authentication

Role-based permissions

Form input validation

Secure logout

⚙️ How It Works

Users register with a username, email, and password

Posts are stored locally in /posts as .md files

Markdown is rendered into HTML for display

SQLite database stores user accounts & roles

Admins have complete control over posts & accounts

📜 License

This project is open-source — you may use, modify, and share it for learning or personal projects.
