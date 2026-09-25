from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict
import os

from app.solver import solve_wfm_schedule

app = FastAPI(title="Call Center WFM Scheduler")
templates = Jinja2Templates(directory="app/templates")

class ScheduleRequest(BaseModel):
    num_employees: int
    days: int
    shifts_per_day: int
    min_coverage: List[List[int]]
    preferences: List[Dict[str, int]] = []

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    env_name = os.getenv("ENVIRONMENT", "dev")
    # Updated to pass request as an explicit keyword argument to support modern Starlette/FastAPI
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"env": env_name}
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": os.getenv("ENVIRONMENT", "dev")}

@app.post("/api/v1/schedule")
async def generate_schedule(req: ScheduleRequest):
    try:
        result = solve_wfm_schedule(
            num_employees=req.num_employees,
            days=req.days,
            shifts_per_day=req.shifts_per_day,
            min_coverage=req.min_coverage,
            preferences=req.preferences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))