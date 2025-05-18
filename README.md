# 📊 installation-app

A full-stack web application that collects and visualizes visitor event analytics. Built with **Vue 3 + Chart.js** on the frontend and **FastAPI + SQLite** on the backend.

---

## 🔧 Tech Stack

- **Frontend**: Vue 3 (Composition API), Chart.js
- **Backend**: FastAPI, SQLite
- **Styling**: SCSS
- **Communication**: REST API with CORS enabled

---

## 📊 Features

### Frontend
- 📈 **Metrics Dashboard**: View event counts per installation and event type
- 🧠 **Popular Installations**: Pie chart of most active installations
- 📋 **Events List**: Full event log with timestamp and installation info

### Backend
- 🔁 REST API to receive and serve event data
- 💾 SQLite database to persist events
- 🧩 Grouping and aggregation endpoints:
    - `/metrics`
    - `/popular_installations`
    - `/events`

---

## 🚀 Getting Started

### 1. Clone the Repository


git clone https://github.com/your-username/installation-app.git  
cd installation-app


# Start Backend
 - Requires Python 3.8+

```bash
 $ cd backend  
 $ pip install fastapi uvicorn pydantic  
 $ uvicorn main:app --reload
```

# Start Frontend
 - Requires Node.js 18+ and Vite

```bash
 $ cd frontend  
 $ npm install  
 $ npm run dev
```

The API will be available at:
👉 http://127.0.0.1:8000

# 📂 Project Structure
```bash

├── frontend/               # Vue 3 frontend with Chart.js
│   └── App.vue             # Main dashboard page
├── backend/                # FastAPI backend
│   └── main.py             # API and DB logic
└── events.db               # SQLite database (created at runtime)
```
# 📬 API Endpoints
```bash
| Method | Endpoint                 | Description               |
| ------ | ------------------------ | ------------------------- |
| POST   | `/event`                 | Submit a new event        |
| GET    | `/metrics`               | Grouped event metrics     |
| GET    | `/events`                | List all events           |
| GET    | `/popular_installations` | Most active installations |
```

# 🧪 Example Payload
```bash
├── frontend/               # Vue 3 frontend with Chart.js
│   └── App.vue             # Main dashboard page
├── backend/                # FastAPI backend
│   └── main.py             # API and DB logic
└── events.db               # SQLite database (created at runtime)
```
