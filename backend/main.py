import os
import psycopg
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

DB = os.environ["DATABASE_URL"]
app = FastAPI()

def get_db_connection():
    return psycopg.connect(DB)

def init_db():
    with get_db_connection() as conn:  
        conn.execute("CREATE TABLE IF NOT EXISTS work_logs (id SERIAL PRIMARY KEY, employee_name VARCHAR(100), date DATE, start_hour TEXT, end_hour TEXT, description TEXT DEFAULT '')")
    return 0

init_db()

class WorkLog(BaseModel):
    employee_name: str
    date: str
    start_hour: str
    end_hour: str
    description: str = ""

@app.post("/logs")
def create_log(log: WorkLog):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO work_logs (employee_name, date, start_hour, end_hour, description) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (log.employee_name, log.date, log.start_hour, log.end_hour, log.description))
            new_id = cur.fetchone()[0]
        return {"id": new_id, "message":"Zapisano pomyślnie"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/logs")
def get_logs():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, employee_name, date, start_hour, end_hour, description FROM work_logs ORDER BY date DESC, id DESC")
            rows = cur.fetchall()
        logs = []
        for row in rows:
            logs.append({"id": row[0], "employee_name": row[1], "date": row[2], "start_hour": row[3], "end_hour": row[4], "description": row[5]})
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
