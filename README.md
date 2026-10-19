# 🌙 NOCTRA — Social Media Platform

**NOCTRA** is a Django-based social media platform designed to help users connect, share posts, interact with other users, and manage their privacy.

The project demonstrates the development of a social networking application with user authentication, content sharing, social interactions, notifications, and direct messaging.

---

## ✨ Features

### 👤 User Authentication
- User registration
- User login
- User account access

### 📝 Posts and Social Interaction
- Community feed
- Create and share posts
- Like and unlike posts
- Follow other users
- Explore users and content

### 👥 User Profiles
- User profile pages
- Edit profile functionality
- Profile-based content display

### 🔔 Notifications
- Notifications section for social interactions

### 💬 Direct Messaging
- Messaging interface
- Inbox and chat pages

### 🔒 Privacy Management
- Private account settings
- Privacy-aware profile content visibility

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| HTML | Web page structure |
| CSS | Styling and user interface |
| SQLite | Database |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📁 Project Structure

```text
NOCTRA/
│
├── accounts/
│   ├── migrations/
│   └── templates/
│
├── posts/
│   ├── migrations/
│   └── templates/
│
├── messaging/
│   ├── migrations/
│   └── templates/
│
├── notifications/
│   ├── migrations/
│   └── templates/
│
├── noctra/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── socialfeed/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

Follow these steps to run NOCTRA locally.

### 1. Clone the Repository

```bash
git clone https://github.com/haniya-sabrin/NOCTRA.git
```

Navigate into the project directory:

```bash
cd NOCTRA
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your Django secret key:

```env
SECRET_KEY=your_django_secret_key
```

Replace the placeholder with a valid Django secret key.

**Security note:** Never upload your `.env` file or expose your actual secret key publicly.

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

---

## 🎯 Project Objective

The objective of NOCTRA is to develop a social media platform using Django that demonstrates web application development, user authentication, social interaction, communication interfaces, and privacy management.

---

## 🚀 Learning Outcomes

This project provides practical experience with:

- Django application development
- Python backend programming
- Database models and migrations
- URL routing and views
- HTML templates
- User authentication workflows
- Social media feature development
- Environment variable management
- Git and GitHub version control

---

## 👩‍💻 Developer

**Haniya Sabrin A**

GitHub: [haniya-sabrin](https://github.com/haniya-sabrin)

---

## 📌 Project Status

Developed as a learning and portfolio project.

---

## 🔗 Repository

Explore the source code:

[NOCTRA — GitHub Repository](https://github.com/haniya-sabrin/NOCTRA)

---
