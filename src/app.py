"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Train for competitive soccer matches and team drills",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "isabella@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Practice swimming techniques and prepare for swim meets",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Work on shooting, passing, and team plays for basketball competitions",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["matt@mergington.edu", "nina@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Develop volleyball skills, team coordination, and match strategies",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["jordan@mergington.edu", "hannah@mergington.edu"]
    },
    "Track and Field": {
        "description": "Train in running, jumping, and throwing events for school meets",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 24,
        "participants": ["ryan@mergington.edu", "sophie@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Practice tennis skills, match play, and racket techniques",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["carter@mergington.edu", "lily@mergington.edu"]
    },
    "Yoga Club": {
        "description": "Develop flexibility, balance, and mindfulness through yoga practice",
        "schedule": "Mondays and Fridays, 2:30 PM - 3:30 PM",
        "max_participants": 20,
        "participants": ["haley@mergington.edu", "noel@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["mia@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Build acting skills, rehearse scenes, and stage performances",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques and create visual storytelling projects",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["zoe@mergington.edu", "miles@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Practice musical pieces together and prepare for performances",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["harper@mergington.edu", "leo@mergington.edu"]
    },
    "Creative Writing Club": {
        "description": "Write stories, poetry, and essays while sharing feedback with peers",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "jarrett@mergington.edu"]
    },
    "Dance Troupe": {
        "description": "Learn choreography, improve dance skills, and perform together",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 18,
        "participants": ["madison@mergington.edu", "tyler@mergington.edu"]
    },
    "Ceramics Workshop": {
        "description": "Create pottery pieces, learn glazing techniques, and explore ceramics",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["luna@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare arguments, practice public speaking, and debate current topics",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments, discuss discoveries, and explore scientific ideas",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["oliver@mergington.edu", "emma@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design and build robots while learning engineering and programming",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["nina@mergington.edu", "caleb@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems, prepare for contests, and explore new concepts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ethan@mergington.edu", "ava@mergington.edu"]
    },
    "Astronomy Society": {
        "description": "Study stars, planets, and space topics through observation and discussion",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["zoe@mergington.edu", "miles@mergington.edu"]
    },
    "Environmental Science Club": {
        "description": "Explore environmental issues, conservation projects, and sustainability ideas",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu", "hannah@mergington.edu"]
    },
    "History Discussion Group": {
        "description": "Discuss historical events, research topics, and learn from the past",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["harper@mergington.edu", "alex@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
