Markdown Blog

A lightweight local Markdown blogging platform built with Python Flask featuring user authentication, role-based access control, and a modern social-media-style interface.

Features

User Authentication – Register, log in, and manage accounts securely

Role-Based Access – Regular users can create and manage their own posts; Admins have full content and user management

Secure Authentication – Password hashing and session management

Post Management – Create, edit, and delete Markdown posts

Local Storage – Posts saved as .md files in a local folder

Markdown Rendering – Converts .md to HTML for display

Search System – Find posts by title

Like Feature – One like per user per post

Responsive UI – Mobile-friendly layout using Bootstrap

Requirements

Python 3.7+

Flask

Flask-SQLAlchemy

Markdown

Werkzeug

Install dependencies:

pip install -r requirements.txt

Getting Started

Clone the repository:

git clone <repo_url>
cd markdown-blog


Install dependencies:

pip install -r requirements.txt


Run the app:

python app.py


Open http://localhost:5000 in your browser

Default Admin Account

Username: admin
Password: admin123
(Created automatically on first run)

User Roles

Regular Users:

Create & view blog posts

Search posts

Manage profile & change password

Delete their own posts

Cannot edit existing posts

Cannot delete other users’ posts

Administrators:

All regular user privileges

Edit/delete any post

View all registered users

Grant/revoke admin privileges

Delete user accounts

Access the Admin Dashboard

File Structure
project/
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

Security Features

Password Hashing (Werkzeug)

Session-Based Authentication

Form Input Validation

Role-Based Permissions

Secure Logout

How It Works

Users register with a username, email, and password. Posts are stored as Markdown files in the posts folder. Markdown is converted to HTML for display. SQLite stores user accounts and roles. Admin users have full control over posts and accounts.

API Endpoints

Public & User Routes:

GET / → Homepage with all posts

GET /post/<filename> → View a post

GET /create → Create post (login required)

POST /create → Submit new post

GET /search → Search posts

Admin Routes:

GET /edit/<filename> → Edit post

POST /edit/<filename> → Save edits

GET /admin/users → View all users

POST /admin/user/<id>/toggle-admin → Change role

POST /admin/user/<id>/delete → Delete user

Like System:

POST /like/<filename> → Like/unlike post

GET /post/<filename>/likes → Get like count

License

This project is open-source. Feel free to use, modify, and share it for learning or personal projects.
