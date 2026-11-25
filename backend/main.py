import os
import psycopg
import re
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

DB = os.environ["DATABASE_URL"]
app = FastAPI(root_path="/api")

def get_db_connection():
    return psycopg.connect(DB)

class WorkLog(BaseModel):
    first_name: str
    last_name: str
    date: str
    start_hour: str
    end_hour: str
    description: str = ""

@app.get("/health")
def health():
    with get_db_connection() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}

@app.post("/log")
def create_log(log: WorkLog):
    pattern_hour = r"([01]\d|2[0-3]):[0-5]\d"
    pattern_date = r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"
    pattern_first_name = r"[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?: [A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)*"
    pattern_last_name = r"[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:[- ][A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)*"
    if not re.fullmatch(pattern_hour, log.start_hour) or not re.fullmatch(pattern_hour, log.end_hour):
        raise HTTPException(status_code=400, detail="Niepoprawny format godziny. Poprawny format: HH:MM")
    if not re.fullmatch(pattern_date, log.date):
        raise HTTPException(status_code=400, detail="Niepoprawny format daty. Poprawny format: YYYY-MM-DD")
    if not re.fullmatch(pattern_first_name, log.first_name):
        raise HTTPException(status_code=400, detail="Niepoprawny format imienia.")
    if not re.fullmatch(pattern_last_name, log.last_name):
        raise HTTPException(status_code=400, detail="Niepoprawny format nazwiska.")
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO work_logs (first_name, last_name, date, start_hour, end_hour, description) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (log.first_name, log.last_name, log.date, log.start_hour, log.end_hour, log.description))
            new_id = cur.fetchone()[0]
        return {"id": new_id, "message": "Zapisano pomyślnie"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/logs")
def get_logs():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, first_name, last_name, date, start_hour, end_hour, description FROM work_logs ORDER BY date DESC, id DESC")
            rows = cur.fetchall()
        logs = []
        for row in rows:
            logs.append({"id": row[0], "first_name": row[1], "last_name": row[2], "date": row[3], "start_hour": row[4], "end_hour": row[5], "description": row[6]})
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/log/{id}")
def get_log(id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, first_name, last_name, date, start_hour, end_hour, description FROM work_logs WHERE id = %s", (id,))
            row = cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Log nie istnieje")
            return {"id": row[0], "first_name": row[1], "last_name": row[2], "date": row[3], "start_hour": row[4], "end_hour": row[5], "description": row[6]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
