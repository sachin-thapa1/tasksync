# 📋 TaskSync Manager

**Backend Developer | Django | Task Management Project**

A **Task Management System** built with **Django** and **PostgreSQL**. TaskSync Manager allows users to manage their daily tasks, track progress, and maintain user profiles with role-based access control.

---

## 🛠️ Tech Stack

**Backend:**  
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)

**Database:**  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)

**Tools:**  
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)  
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=postman&logoColor=white)  

---

## 🚀 Features

- ✅ **User Authentication & Authorization**  
  - Login, Logout, and Registration functionality  
- ✅ **Task Management**  
  - Create, edit, delete, and mark tasks as complete  
- ✅ **User Profiles**  
  - Users can edit their profile information  
- ✅ **Admin Controls**  
  - Admins can delete any user  
- ✅ **Dashboard**  
  - Shows all tasks assigned to the logged-in user  
- ✅ **RESTful & Secure**  
  - Proper HTTP methods for actions, with role-based restrictions  

---

## 🔗 API Endpoints

**Authentication & Users**  
- `GET/POST /login/` → User login  
- `GET /logout/` → Logout user  
- `GET/POST /register/` → User registration  
- `GET/POST /profile/<user_id>/edit/` → Edit user profile  
- `POST /user/<user_id>/delete/` → Delete a user (Admin only)  

**Tasks**  
- `GET /dashboard/` → User dashboard showing tasks  
- `POST /task/<task_id>/complete/` → Mark task as complete  
- `POST /task/<task_id>/delete/` → Delete a task  
- `GET/POST /task/<task_id>/edit/` → Edit a task  

> Note: All endpoints require proper authentication for access.

---

## ⚡ Installation

1. Clone the repo:

```bash
git clone https://github.com/sachin-thapa1/tasksync-manager.git
Live api : tasksync-n1na.onrender.com
cd tasksync-manager
