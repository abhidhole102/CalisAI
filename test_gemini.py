import os
import json
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

athlete_profile = {
    "fitness_level": "Intermediate",
    "pull_ups": 12,
    "dips": 20,
    "push_ups": 30,
    "goal": "Muscle-Up",
    "training_days": 4,
    "equipment": "Pull-up bar and parallel bars",
    "current_skill": "Chest-to-bar pull-up"
}

prompt = f"""
You are CalisAI, a personalized calisthenics workout recommendation system.

Analyze this athlete profile:

{athlete_profile}

Create a personalized workout plan.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "fitness_level": "Intermediate",
    "goal": "Muscle-Up",
    "summary": "Short explanation of the plan",
    "days": [
        {{
            "day": 1,
            "focus": "Explosive Pull and Skill",
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
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

text = response.text.strip()

print(text)