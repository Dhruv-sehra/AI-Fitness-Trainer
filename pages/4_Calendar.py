import ast
import json
import re
import streamlit as st
from streamlit_calendar import calendar
from Homepage import set_sidebar_visibility  


st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆")



transferred_value = st.session_state.get('transferred_variable')


def extract_calendar_text(text: str):
    if not isinstance(text, str):
        return None
    text = text.strip()
    if text.startswith("```"):
        if "```" in text[3:]:
            _, _, text = text.partition("```")
        text = text.rstrip("`").strip()
    if not text:
        return None
    if "[" in text and "]" in text:
        start = text.find("[")
        end = text.rfind("]")
        return text[start:end + 1]
    if "{" in text and "}" in text:
        start = text.find("{")
        end = text.rfind("}")
        return text[start:end + 1]
    return text


def parse_calendar_data(transferred_value):
    if isinstance(transferred_value, list):
        return transferred_value
    if isinstance(transferred_value, str):
        candidate = extract_calendar_text(transferred_value)
        if candidate is None:
            return None
        candidate = candidate.replace('“', '"').replace('”', '"')
        try:
            return json.loads(candidate)
        except Exception:
            try:
                return ast.literal_eval(candidate)
            except Exception:
                return None
    return None


events = parse_calendar_data(transferred_value)
if events is None:
    if transferred_value is not None:
        st.warning("Saved calendar data is not valid JSON or Python list. Please submit a new plan.")
    events = []

mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "timeline",
        "resource-daygrid",
        "resource-timegrid",
        "resource-timeline",
        "list",
        "multimonth",
    ),
)


calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]
calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": calendar_resources,
    "selectable": "true",
}

if "resource" in mode:
    if mode == "resource-daygrid":
        calendar_options = {
            **calendar_options,
            "initialDate": "2026-07-01",
            "initialView": "resourceDayGridDay",
            "resourceGroupField": "building",
        }
    elif mode == "resource-timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "initialDate": "2026-07-01",
            "initialView": "resourceTimelineDay",
            "resourceGroupField": "building",
        }
    elif mode == "resource-timegrid":
        calendar_options = {
            **calendar_options,
            "initialDate": "2026-07-01",
            "initialView": "resourceTimeGridDay",
            "resourceGroupField": "building",
        }
else:
    if mode == "daygrid":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": "2026-07-01",
            "initialView": "dayGridMonth",
        }
    elif mode == "timegrid":
        calendar_options = {
            **calendar_options,
            "initialView": "timeGridWeek",
        }
    elif mode == "timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timelineDay,timelineWeek,timelineMonth",
            },
            "initialDate": "2026-07-01",
            "initialView": "timelineMonth",
        }
    elif mode == "list":
        calendar_options = {
            **calendar_options,
            "initialDate": "2026-07-01",
            "initialView": "listMonth",
        }
    elif mode == "multimonth":
        calendar_options = {
            **calendar_options,
            "initialView": "multiMonthYear",
        }

state = calendar(
    events= events,
    options=calendar_options,
    custom_css="""
    .fc-event-title {
        color: black; /* Set text color to black */
    }
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key=mode,
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

#st.write(state)

#st.markdown("## API reference")
# st.help(calendar)
