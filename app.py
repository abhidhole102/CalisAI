from flask import Flask, render_template, request, jsonify
import os
import time
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

   

    goal_strategies = {

    "Build Strength": """
Focus on balanced full-body strength.
Prioritize pushing strength, pulling strength,
lower-body strength and core stability.
Use progressive bodyweight exercises appropriate
for the athlete's level.
""",

    "Muscle-Up": """
Focus primarily on explosive pulling power,
high pull-ups, chest-to-bar strength,
transition mechanics and straight-bar pushing strength.
""",

    "Handstand": """
Focus on shoulder strength, wrist preparation,
handstand line, balance and progressive freestanding practice.
""",

    "Handstand Push-Up": """
Focus on overhead pushing strength, pike push-ups,
wall handstand control, eccentric HSPU work and shoulder stability.
""",

    "Planche": """
Focus on straight-arm pushing strength,
scapular protraction, planche leans,
pseudo planche push-ups and progressive planche holds.
""",

    "Front Lever": """
Focus on straight-arm pulling strength,
scapular control, tuck front lever progressions,
front lever rows and core tension.
"""
}

    goal_strategy = goal_strategies.get(
    goal,
    goal_strategies["Build Strength"]
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
You are CalisAI, an intelligent personalized calisthenics workout recommendation system.

Your job is to create a safe, practical and highly personalized training plan.


ATHLETE PROFILE:

{athlete_profile}

GOAL-SPECIFIC STRATEGY:

{goal_strategy}

PERSONALIZATION RULES:

1. Use the athlete's fitness level as the baseline for exercise difficulty.

2. Use the athlete's pull-ups, dips and push-ups to estimate their current strength.

3. Consider the athlete's primary goal and make the majority of training directly support that goal.

4. Consider the athlete's current skill.
   Do NOT recommend basic progressions for skills the athlete has already mastered.

5. STRICTLY respect the available equipment.
   Do not recommend equipment that the athlete does not have.

6. Respect the number of training days selected by the athlete.
   Generate exactly that many training days.

7. Adjust exercise difficulty to the athlete's current ability.
   Avoid unnecessarily advanced exercises for beginners.

8. Include appropriate rest periods based on exercise difficulty.

9. Prioritize skill practice, strength development and progression relevant to the athlete's goal.

10. Do not simply return a generic workout.
    Every part of the plan should be influenced by the athlete profile.

11. If the athlete already has a prerequisite skill, move to the next appropriate progression.

12. Keep the workout practical for real-world calisthenics training.

13. Follow the goal-specific strategy when selecting exercises and structuring the workout.

14. STRICT EQUIPMENT RULE:
    Use ONLY the equipment listed in the athlete profile.

    Never recommend equipment that the athlete does not have.

    For example, if the athlete has only:
    - Pull-up bar
    - Parallel bars

    then do NOT recommend:
    - Weighted pull-ups
    - Weighted dips
    - Dumbbells
    - Barbells
    - Resistance bands
    - Gym machines
    - Weight plates

    Bodyweight and floor exercises are always allowed.

    If an exercise normally requires equipment that is not available,
    replace it with a suitable bodyweight alternative.

    15. Before returning the final JSON, verify every exercise against
    the athlete's available equipment. Remove or replace any exercise
    that requires unavailable equipment.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "fitness_level": "{level}",
    "goal": "{goal}",
    "summary": "Short explanation of why this plan is appropriate for this athlete.",

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
        "Technique tip 2",
        "Technique tip 3"
    ]
}}

IMPORTANT:

- Return exactly {training_days} training days.
- Do not invent equipment.
- Do not ignore the athlete's current skill.
- Do not recommend progressions that are clearly below the athlete's demonstrated ability.
- Keep the plan realistic and progressive.
- Return JSON only. Do not include markdown or explanations outside the JSON.
"""
    try:
        start_time = time.time()
        ai_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        end_time = time.time()

        print("Gemini response time:", round(end_time - start_time, 2), "seconds")

        ai_text = ai_response.text.strip()
        ai_workout = json.loads(ai_text)

    except Exception as e:
        print("Gemini API Error:", e)

        error_message = str(e)

        # Gemini quota/rate limit
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return jsonify({
                "error": "AI_LIMIT",
                "message": "Gemini API limit reached. Please try again later."
            }), 429

        # Gemini temporary server overload
        elif "503" in error_message or "UNAVAILABLE" in error_message:
            return jsonify({
                "error": "AI_UNAVAILABLE",
                "message": "AI service is temporarily busy. Please try again in a moment."
            }), 503

        # Invalid AI response / JSON problem
        elif "JSON" in error_message or "json" in error_message:
            return jsonify({
                "error": "AI_RESPONSE_ERROR",
                "message": "AI generated an invalid workout response. Please try again."
            }), 500

        # Any other unexpected error
        else:
            return jsonify({
                "error": "AI_ERROR",
                "message": "Something went wrong while generating your workout."
            }), 500

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