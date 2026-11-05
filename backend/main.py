from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return 0

def init_db():
    return 0

@app.on_event("startup")
def startup():
    try:
        init_db()
    except Exception as e:
        print(f"Błąd połączenia z BD: {e}")


class WorkLog(BaseModel):
    employee_name: str
    date: str
    start_hour: int
    end_hour: int
    description: str = ""

@app.post("/logs")
def create_log(log: WorkLog):
    try:
        conn = get_db_connection()
        
        # cur = conn.cursor()
        # cur.execute() # DODAĆ INSERT INTO dla loga
        # new_id = cur.fetchone()[0]
        # conn.commit()
        # cur.close()
        # conn.close()
        # return {"id": new_id, "message":"Zapisano pomyślnie"}
        return 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/logs")
def get_logs():
    try:
        conn = get_db_connection()
        # cur = conn.cursor()
        # cur.execute() # DODAĆ INSERT INTO dla loga
        rows = [[0]*6]*100 # rows = cur.fetchall()
        # cur.close()
        # conn.close()
        
        logs = []

        for row in rows:
            logs.append({
                "id": row[0],
                "employee_name": row[1],
                "date": row[2],
                "start_hour": row[3],
                "end_hour": row[4],
                "description": row[5],
            })
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, details=str(e))