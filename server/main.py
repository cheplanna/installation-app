from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
import sqlite3

app = FastAPI(title="Visitor Analytics API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:5173"] for specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
def init_db():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            installation_id TEXT,
            event_type TEXT,
            timestamp TEXT,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Pydantic model for events
class Event(BaseModel):
    installation_id: str
    event_type: str
    timestamp: Optional[datetime] = datetime.utcnow()
    details: Optional[Dict] = {}

@app.post("/event")
async def receive_event(event: Event):
    try:
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (installation_id, event_type, timestamp, details)
            VALUES (?, ?, ?, ?)
        ''', (event.installation_id, event.event_type, event.timestamp.isoformat(), str(event.details)))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    try:
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT installation_id, event_type, COUNT(*) as count
            FROM events
            GROUP BY installation_id, event_type
        ''')
        rows = cursor.fetchall()
        conn.close()

        metrics = []
        for row in rows:
            metrics.append({
                "installation_id": row[0],
                "event_type": row[1],
                "count": row[2]
            })

        return {"metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_all_events():
    try:
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM events''')
        rows = cursor.fetchall()
        conn.close()

        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "installation_id": row[1],
                "event_type": row[2],
                "timestamp": row[3],
                "details": row[4]
            })

        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/popular_installations")
async def get_popular_installations():
    try:
        conn = sqlite3.connect("events.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT installation_id, COUNT(*) as event_count
            FROM events
            GROUP BY installation_id
            ORDER BY event_count DESC
        ''')
        rows = cursor.fetchall()
        conn.close()

        result = [{"installation_id": row[0], "event_count": row[1]} for row in rows]
        return {"popular_installations": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
