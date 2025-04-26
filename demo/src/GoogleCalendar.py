"""
GoogleCalendarEnhanced.py – list / export / bulk‑import / delete Google Calendar

Usage
-----
# List events and dump current state to **calendar_events.json**
$ python GoogleCalendarEnhanced.py

# Bulk‑insert events from a JSON file
$ python GoogleCalendarEnhanced.py new_events.json

# Bulk‑delete events described in a JSON file
$ python GoogleCalendarEnhanced.py --delete delete_events.json

JSON formats
------------
* **Insert file** (`new_events.json`)
  [
    {"title":"Demo",
     "start":"2025-05-10T09:00:00+02:00",
     "end"  :"2025-05-10T10:00:00+02:00",
     "description":"…", "location":"…"},
    …
  ]

* **Delete file** (`delete_events.json`)
  Option A – by *eventId* (always succeeds if the ID exists):
  [
    {"id":"6qv2u3i4j9bkf0q3a9…"},
    {"id":"0bq5u9e4gc1e1p6k7…"}
  ]

  Option B – by time window (and optional title match):
  [
    {"start":"2025-05-10T09:00:00+02:00",
     "end"  :"2025-05-10T10:00:00+02:00",
     "title":"Demo"}
  ]
"""

from __future__ import annotations
import os, sys, json, pathlib, urllib.parse
from datetime import timezone, timedelta
from dateutil import parser
from urllib.parse import quote

# ─── Google client libs ──────────────────────────────────────────────────────
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── CONFIG ──────────────────────────────────────────────────────────────────
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CLIENT_SECRET = "client_secret.json"  # OAuth client file
TOKEN_FILE = "token.json"  # generated after first run
CAL_ID = "primary"  # calendar to work with
PLUS2 = timezone(timedelta(hours=2))  # UTC+2 (Warsaw)


# ─── AUTH ────────────────────────────────────────────────────────────────────

def get_credentials():
    """Return valid OAuth2 credentials (refresh or run flow if needed)."""
    creds: Credentials | None = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0, prompt="consent")
        with open(TOKEN_FILE, "w", encoding="utf-8") as fh:
            fh.write(creds.to_json())
    return creds


def get_calendar_service():
    return build("calendar", "v3", credentials=get_credentials(), cache_discovery=False)


# ─── LIST / EXPORT ──────────────────────────────────────────────────────────

def pick_date(d: dict) -> str | None:
    return d.get("dateTime") or d.get("date")


def get_planned_dates():
    """Return sorted list of (start_dt, end_dt, title)."""
    service = get_calendar_service()
    events, page_token = [], None
    while True:
        resp = (
            service.events()
            .list(
                calendarId=CAL_ID,
                singleEvents=True,
                showDeleted=False,
                maxResults=2500,
                pageToken=page_token,
            )
            .execute()
        )
        events.extend(resp.get("items", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    planned = []
    for ev in events:
        if ev.get("status") == "cancelled":
            continue
        raw_s, raw_e = pick_date(ev["start"]), pick_date(ev["end"])
        if not (raw_s and raw_e):
            continue
        dt_s = parser.isoparse(raw_s).astimezone(PLUS2)
        dt_e = parser.isoparse(raw_e).astimezone(PLUS2)
        planned.append((dt_s, dt_e, ev.get("summary", "(bez tytułu)")))

    planned.sort(key=lambda t: t[0])
    return planned


def toJSON(events, path="calendar_events.json"):
    payload = [
        {"start": s.isoformat(), "end": e.isoformat(), "title": t}
        for s, e, t in events
    ]
    pathlib.Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return path


# ─── INSERT ────────────────────────────────────────────────────────────────

def create_event_oauth(*, summary, start, end, description="", location="", calendar_id=CAL_ID):
    service = get_calendar_service()
    body = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"dateTime": start.isoformat()},  # keep offset, no timeZone key
        "end": {"dateTime": end.isoformat()},
    }
    return service.events().insert(calendarId=calendar_id, body=body).execute()


def create_plans_from_json(json_path: str, calendar_id: str = CAL_ID):
    data = json.loads(pathlib.Path(json_path).read_text(encoding="utf-8"))
    results = []
    for row in data:
        start = parser.isoparse(row["start"])
        end = parser.isoparse(row["end"])
        resp = create_event_oauth(summary=row["title"],
                                  start=start,
                                  end=end,
                                  description=row.get("description", ""),
                                  location=row.get("location", ""),
                                  calendar_id=calendar_id)
        results.append(resp)
    return results


# ─── DELETE ────────────────────────────────────────────────────────────────

def delete_events_from_json(json_path: str, calendar_id: str = CAL_ID):
    """Delete events listed in *json_path*.

    Accepts two formats:
    1. By Google event **id** → {"id": "…"}
    2. By **time window** (+ optional title) → {"start": "…", "end": "…", "title": "…"}
    Returns list of IDs successfully deleted.
    """
    data = json.loads(pathlib.Path(json_path).read_text(encoding="utf-8"))
    service = get_calendar_service()
    deleted: list[str] = []

    for row in data:
        # ── 1) delete by explicit eventId ───────────────────────────────────
        if "id" in row:
            try:
                service.events().delete(calendarId=calendar_id, eventId=row["id"]).execute()
                deleted.append(row["id"])
            except HttpError as e:
                print(f"Could not delete {row['id']}: {e}")
            continue

        # ── 2) delete by time window (+ optional title) ─────────────────────
        if not ("start" in row and "end" in row):
            print("Skip row – needs either 'id' or 'start' and 'end'.")
            continue
        start = parser.isoparse(row["start"])
        end = parser.isoparse(row["end"])
        matches = (
            service.events()
            .list(calendarId=calendar_id,
                  timeMin=start.isoformat(),
                  timeMax=end.isoformat(),
                  singleEvents=True)
            .execute()
            .get("items", [])
        )
        for ev in matches:
            if "title" in row and row["title"] != ev.get("summary", ""):
                continue  # title mismatch → keep event
            try:
                service.events().delete(calendarId=calendar_id, eventId=ev["id"]).execute()
                deleted.append(ev["id"])
            except HttpError as e:
                print(f"Could not delete {ev['id']}: {e}")

    return deleted


# ─── CLI ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # default: bulk‑insert
        booked = create_plans_from_json(sys.argv[1])
        print(f"Created {len(booked)} events.")

    elif len(sys.argv) == 3 and sys.argv[1] == "--delete" and sys.argv[2].endswith(".json"):
        deleted = delete_events_from_json(sys.argv[2])
        print(f"Deleted {len(deleted)} events.")

    else:
        # list + dump current calendar
        evts = get_planned_dates()
        print(f"Łącznie zdarzeń: {len(evts)}")
        for s, e, t in evts:
            print(f"{s:%Y-%m-%d %H:%M} — {e:%H:%M}  |  {t}")
        print("Zapisano do:", toJSON(evts))
