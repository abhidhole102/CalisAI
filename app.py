from flask import Flask, render_template, request, jsonify
import os
import json
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def generate_workout(level, goal, training_days):

    workouts = {

        "Muscle-Up": [
            {
                "name": "Explosive Pull-Ups",
                "sets": 3,
                "reps": "5-8",
                "rest": "2-3 min"
            },
            {
                "name": "Chest-to-Bar Pull-Ups",
                "sets": 3,
                "reps": "5-8",
                "rest": "2 min"
            },
            {
                "name": "High Pulls",
                "sets": 3,
                "reps": "4-6",
                "rest": "2-3 min"
            },
            {
                "name": "Transition Drills",
                "sets": 3,
                "reps": "5-8",
                "rest": "90 sec"
            }
        ],

        "Handstand": [
            {
                "name": "Wall Handstand",
                "sets": 3,
                "reps": "20-40 sec",
                "rest": "60-90 sec"
            },
            {
                "name": "Pike Holds",
                "sets": 3,
                "reps": "20-30 sec",
                "rest": "60 sec"
            },
            {
                "name": "Wall Shoulder Taps",
                "sets": 3,
                "reps": "6-10",
                "rest": "90 sec"
            },
            {
                "name": "Freestanding Balance",
                "sets": 4,
                "reps": "10-20 sec",
                "rest": "90 sec"
            }
        ],

        "Planche": [
            {
                "name": "Planche Lean",
                "sets": 4,
                "reps": "15-25 sec",
                "rest": "2 min"
            },
            {
                "name": "Pseudo Planche Push-Ups",
                "sets": 3,
                "reps": "6-10",
                "rest": "2 min"
            },
            {
                "name": "Tuck Planche",
                "sets": 4,
                "reps": "8-15 sec",
                "rest": "2-3 min"
            },
            {
                "name": "Advanced Tuck",
                "sets": 3,
                "reps": "5-10 sec",
                "rest": "2-3 min"
            }
        ],

        "Front Lever": [
            {
                "name": "Scapular Pulls",
                "sets": 3,
                "reps": "8-12",
                "rest": "90 sec"
            },
            {
                "name": "Tuck Front Lever",
                "sets": 4,
                "reps": "10-20 sec",
                "rest": "2 min"
            },
            {
                "name": "Advanced Tuck",
                "sets": 3,
                "reps": "8-15 sec",
                "rest": "2 min"
            },
            {
                "name": "Front Lever Rows",
                "sets": 3,
                "reps": "5-8",
                "rest": "2-3 min"
            }
        ],

        "Handstand Push-Up": [
            {
                "name": "Pike Push-Ups",
                "sets": 3,
                "reps": "8-12",
                "rest": "90 sec"
            },
            {
                "name": "Elevated Pike Push-Ups",
                "sets": 3,
                "reps": "6-10",
                "rest": "2 min"
            },
            {
                "name": "Wall Handstand",
                "sets": 3,
                "reps": "20-40 sec",
                "rest": "90 sec"
            },
            {
                "name": "Negative HSPU",
                "sets": 3,
                "reps": "3-5",
                "rest": "2-3 min"
            }
        ],

        "Build Strength": [
            {
                "name": "Push-Ups",
                "sets": 3,
                "reps": "8-15",
                "rest": "90 sec"
            },
            {
                "name": "Pull-Ups",
                "sets": 3,
                "reps": "5-10",
                "rest": "2 min"
            },
            {
                "name": "Dips",
                "sets": 3,
                "reps": "6-12",
                "rest": "2 min"
            },
            {
                "name": "Squats",
                "sets": 3,
                "reps": "12-20",
                "rest": "90 sec"
            }
        ]
    }

    return workouts.get(
        goal,
        workouts["Build Strength"]
    )

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():

    # Get data sent by JavaScript
    data = request.json

    pull_ups = data["pullUps"]
    dips = data["dips"]
    push_ups = data["pushUps"]
    goal = data["goal"]
    training_days = data["trainingDays"]
    equipment = data["equipment"]
    current_skill = data["currentSkill"]

    # Determine fitness level
    level = "Beginner"

    if pull_ups >= 10 and dips >= 15 and push_ups >= 25:
        level = "Intermediate"

    if pull_ups >= 15 and dips >= 25 and push_ups >= 40:
        level = "Advanced"

    # Generate workout
    workout = generate_workout(
        level,
        goal,
        training_days
    )

    # Create athlete profile
    athlete_profile = {
        "fitness_level": level,
        "pull_ups": pull_ups,
        "dips": dips,
        "push_ups": push_ups,
        "goal": goal,
        "training_days": training_days,
        "equipment": equipment,
        "current_skill": current_skill
    }

    prompt = f"""
You are CalisAI, a personalized calisthenics workout recommendation system.

Analyze the following athlete profile:

{athlete_profile}

Create a personalized workout plan based on the athlete's
current ability, goal, training frequency, equipment, and skill.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "fitness_level": "{level}",
    "goal": "{goal}",
    "summary": "Short explanation of the plan",
    "days": [
        {{
            "day": 1,
            "focus": "Training focus",
            "exercises": [
                {{
                    "name": "Exercise name",
                    "sets": 3,
                    "reps": "5-8",
                    "rest": "2 min"
                }}
            ]
        }}
    ],
    "progression": [
        "Step 1",
        "Step 2",
        "Step 3"
    ],
    "tips": [
        "Technique tip 1",
        "Technique tip 2"
    ]
}}

Keep the workout practical and appropriate for the athlete's
current level.
"""
    ai_response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
    ai_text = ai_response.text.strip()
    ai_workout = json.loads(ai_text)

    # Send result back to JavaScript
    return jsonify({
        "level": level,
        "goal": goal,
        "trainingDays": training_days,
        "equipment": equipment,
        "currentSkill": current_skill,
        "athleteProfile": athlete_profile,
        "workout": workout,
        "aiWorkout": ai_workout
    })


if __name__ == "__main__":
    app.run(debug=True)