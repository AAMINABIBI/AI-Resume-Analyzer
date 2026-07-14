import os
import json
from google import genai
from google.genai import types

# Initialize the Gemini Client (automatically pulls GEMINI_API_KEY from environment)
client = genai.Client()

def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are an expert resume analyzer. 
Analyze the following resume text and provide feedback based on the user's goal: 
User Goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skills for this role.
- Remove irrelevant tools.
- Identify real skill gaps.
- Generate roadmaps only for missing fields.
- Make the output highly specific based on the user's goal.

Resume:
{resume_text}
"""

    try:
        # Define the exact JSON schema Gemini must respond with
        response_schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "skills": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                "missing_skills": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                "roadmap": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                "interview_questions": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
            },
            required=["skills", "missing_skills", "roadmap", "interview_questions"],
        )

        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                system_instruction="You are a strict hiring manager who outputs only JSON matching the requested schema.",
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        # Parse the secure JSON response directly
        return json.loads(response.text)
    
    except Exception as e: 
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }