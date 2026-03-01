from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = None):
    if not q:
        return Response(
            content=json.dumps({"status": "API is running"}, indent=4),
            media_type="application/json"
        )

    q = q.strip()
    result = None

    match = re.search(r"ticket (\d+)", q, re.IGNORECASE)
    if "status" in q.lower() and match:
        ticket_id = int(match.group(1))
        result = {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": ticket_id
            })
        }

    match = re.search(r"on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.", q, re.IGNORECASE)
    if "schedule" in q.lower() and match:
        date, time, meeting_room = match.groups()
        result = {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": meeting_room
            })
        }

    match = re.search(r"employee (\d+)", q, re.IGNORECASE)
    if "expense balance" in q.lower() and match:
        employee_id = int(match.group(1))
        result = {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": employee_id
            })
        }

    match = re.search(r"employee (\d+) for (\d{4})", q, re.IGNORECASE)
    if "performance bonus" in q.lower() and match:
        employee_id, year = match.groups()
        result = {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(employee_id),
                "current_year": int(year)
            })
        }

    match = re.search(r"issue (\d+) for the (.+) department", q, re.IGNORECASE)
    if "report" in q.lower() and match:
        issue_code, department = match.groups()
        result = {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_code),
                "department": department
            })
        }

    if result:
        return Response(
            content=json.dumps(result, indent=4),
            media_type="application/json"
        )

    return Response(
        content=json.dumps({"error": "Invalid query"}, indent=4),
        media_type="application/json",
        status_code=400
    )