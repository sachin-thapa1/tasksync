# TaskSync

A full-stack multi-user task management platform with real-time admin monitoring — built with Django and deployed on Render.

Live: https://tasksync-n1na.onrender.com

> Hosted on Render free tier — may take 30–60 seconds to wake on first request.

---

## What It Is

TaskSync is more than a to-do app. It's a multi-user platform where regular users manage their own tasks, and admins get a live oversight layer — seeing who's online, tracking task completion across all users, and managing the entire user base from a single dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | Django |
| Database | SQLite |
| Frontend | HTML · CSS · JavaScript |
| Deployment | Render |

---

## Features

### All Users
- Register, login, logout with session-based authentication
- Personal dashboard showing own tasks only
- Create tasks with title, description, and due date
- Edit and delete own tasks
- Mark tasks as complete
- Filter tasks — All / Pending / Completed
- Search tasks by keyword
- Real-time task statistics — Total, Completed, Pending
- Recent activity feed — timestamped task completions
- Edit own profile — name, email, avatar upload
- Dark mode toggle

### Admin Only
- View all users — ID, username, role, email, last seen, task count
- Real-time Users Online counter — live session tracking
- Platform-wide Tasks Completed ratio
- View and delete any user's tasks
- Edit or delete any user account
- Full activity feed across all users

---

## Role Overview

| Role | Permissions |
|---|---|
| `User` | Manage own tasks, edit own profile, view own stats |
| `Admin` | Everything above + full user management, platform-wide monitoring |

---

## Pages & Routes

| Route | Access | Description |
|---|---|---|
| `/login/` | Public | Login page with dark mode toggle |
| `/register/` | Public | User registration |
| `/dashboard/` | Authenticated | Main task dashboard |
| `/task/{id}/edit/` | Owner / Admin | Edit a task |
| `/task/{id}/complete/` | Owner / Admin | Mark task complete |
| `/task/{id}/delete/` | Owner / Admin | Delete a task |
| `/profile/{id}/edit/` | Self / Admin | Edit user profile |
| `/user/{id}/delete/` | Admin only | Delete a user |

---

## Getting Started

### Prerequisites
- Python 3.10+

### Setup

**1. Clone the repo**
```bash
git clone https://github.com/sachin-thapa1/tasksync-manager.git
cd tasksync-manager
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Create an admin user**
```bash
python manage.py createsuperuser
```

**6. Start the server**
```bash
python manage.py runserver
```

App available at `http://localhost:8000`.

---

## Status

Active development. Core task management, admin monitoring, session tracking, and user management are fully built and live. Notification system and additional features planned.

---

## License

MIT
