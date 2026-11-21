import os
import psycopg
import re
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

DB = os.environ["DATABASE_URL"]
app = FastAPI(root_path="/api")

def get_db_connection():
    return psycopg.connect(DB)

def init_db():
    with get_db_connection() as conn:  
        conn.execute("CREATE TABLE IF NOT EXISTS work_logs (id SERIAL PRIMARY KEY, employee_name VARCHAR(100), date DATE, start_hour TIME, end_hour TIME, description TEXT DEFAULT '')")
    return 0

init_db()#TODO: lepsze umiejscowienie inicjalizacji bazy danych

class WorkLog(BaseModel):
    employee_name: str
    date: str
    start_hour: str
    end_hour: str
    description: str = ""

@app.get("/health")
def health():
    with get_db_connection() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}

@app.post("/logs")
def create_log(log: WorkLog):
    pattern_hour = r"([01]\d|2[0-3]):[0-5]\d"
    pattern_date = r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"
    if not re.fullmatch(pattern_hour, log.start_hour) or not re.fullmatch(pattern_hour, log.end_hour):
        raise HTTPException(status_code=400, detail="Niepoprawny format godziny. Poprawny format: HH:MM")
    if not re.fullmatch(pattern_date, log.date):
        raise HTTPException(status_code=400, detail="Niepoprawny format daty. Poprawny format: YYYY-MM-DD")
    if log.employee_name.strip() == "":
        raise HTTPException(status_code=400, detail="Pole 'employee_name' nie może być puste")
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO work_logs (employee_name, date, start_hour, end_hour, description) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (log.employee_name, log.date, log.start_hour, log.end_hour, log.description))
            new_id = cur.fetchone()[0]
        return {"id": new_id, "message": "Zapisano pomyślnie"}
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

@app.get("/log/{id}")
def get_log(id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, employee_name, date, start_hour, end_hour, description FROM work_logs WHERE id = %s", (id,))
            row = cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Log nie istnieje")
            return {"id": row[0], "employee_name": row[1], "date": row[2], "start_hour": row[3], "end_hour": row[4], "description": row[5]}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@app.delete("/log/{id}")
def delete_log(id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM work_logs WHERE id = %s RETURNING id", (id,))
            deleted_id = cur.fetchone()
            if deleted_id is None:
                raise HTTPException(status_code=404, detail="Log nie istnieje")
            return {"id": deleted_id[0], "message": "Usunięto pomyślnie"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
