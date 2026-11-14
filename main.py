from fastapi import FastAPI ,Header, HTTPException
from pydantic import BaseModel
import sqlite3
app = FastAPI()

conn = sqlite3.connect("incident.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    service TEXT NOT NULL,
    incident TEXT NOT NULL,
    PRIMARY KEY (service, incident)
)
""")
conn.commit()
class IncidentRequest(BaseModel):
    service: str
    incident: str

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.post("/api/incidents" , status_code = 201)
def incidents(data: IncidentRequest, authorization: str | None = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code = 401, detail = "No Authorize")
    
    if authorization.removeprefix("Bearer ") != "Dev888":
        raise HTTPException(status_code = 403, detail = "Forbidden")
    
    try:
        cursor.execute(
            "INSERT INTO incidents (service, incident) VALUES (?,?)",(data.service , data.incident)
        )
        conn.commit()
        return {"message" : "Incident Reported"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code = 409, detail = "This incident is already reported")
    
@app.get("/api/incidents")
def get_incidents(service: str | None = None):
    if service is not None:
        cursor.execute("SELECT service,incident FROM incidents WHERE service = ?", (service,))
    else:
        cursor.execute("SELECT service,incident FROM incidents")
    rows = cursor.fetchall()

    return {"incidents": rows}

@app.delete("/api/incidents")
def solve_incidents(data: IncidentRequest, authorization: str | None = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code = 401 , detail = "No Authorization")
    if authorization.removeprefix("Bearer ") != "Checker888":
        raise HTTPException(status_code = 403, detail = "Forbidden")
    
    cursor.execute("DELETE FROM incidents WHERE service = ? AND incident = ?",(data.service,data.incident))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "Incident not found")
    return {"message":"Incident Resolve"}
    