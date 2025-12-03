
---

## URL Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login/` | GET/POST | User login page |
| `/logout/` | GET | Logout user |
| `/register/` | GET/POST | User registration |
| `/dashboard/` | GET | User dashboard showing tasks |
| `/task/<task_id>/complete/` | POST | Mark task as complete |
| `/task/<task_id>/delete/` | POST | Delete a task |
| `/task/<task_id>/edit/` | GET/POST | Edit task |
| `/profile/<user_id>/edit/` | GET/POST | Edit profile |
| `/user/<user_id>/delete/` | POST | Delete a user (admin) |

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone <repository_url>
cd tasksync_manager
