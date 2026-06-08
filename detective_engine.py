from google import genai
import json
import re
import os
from dotenv import load_dotenv

# ----------------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------------

load_dotenv()

# ----------------------------------
# GEMINI CLIENT
# ----------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ----------------------------------
# CYBER INVESTIGATION ENGINE
# ----------------------------------

def investigate_message(message):

    prompt = f"""
You are an Expert Cyber Security Threat Analyst.

Analyze the following message carefully.

Message:
{message}

Your task:

1. Identify the most likely cyber threat, scam, fraud, phishing attempt, impersonation attempt, social engineering tactic, or suspicious behavior.
2. Use reasoning and context.
3. Do not rely only on keywords.
4. If the message appears safe, classify it as Safe Message.
5. Assign a realistic confidence score from 0-100.
6. Provide a short explanation.

Return ONLY valid JSON.

{{
    "attack": "",
    "risk": "",
    "confidence": 0,
    "explanation": ""
}}

Rules:

Risk must be one of:
LOW
MEDIUM
HIGH
CRITICAL

No markdown.
No code blocks.
No extra text.
Only JSON.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()

        # Remove markdown if Gemini adds it

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

        # Extract JSON safely

        json_match = re.search(
            r"\{.*\}",
            raw,
            re.DOTALL
        )

        if json_match:
            raw = json_match.group(0)

        result = json.loads(raw)

        attack = result.get(
            "attack",
            "AI Threat Analysis"
        )

        risk = result.get(
            "risk",
            "MEDIUM"
        ).upper()

        confidence = int(
            result.get(
                "confidence",
                50
            )
        )

        explanation = result.get(
            "explanation",
            "AI completed analysis."
        )

        confidence = max(
            0,
            min(confidence, 100)
        )

        # ----------------------------------
        # AUTO GRADE
        # ----------------------------------

        if confidence >= 85:
            grade = "D"

        elif confidence >= 70:
            grade = "C"

        elif confidence >= 50:
            grade = "B"

        else:
            grade = "A+"

        return {

            "attack": attack,
            "risk": risk,
            "confidence": confidence,
            "grade": grade,
            "evidence": [],
            "explanation": explanation

        }

    except Exception:

        # ----------------------------------
        # FALLBACK AI ANALYSIS
        # ----------------------------------

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
Analyze this message and explain whether it appears suspicious.

Message:
{message}

Provide a concise security assessment.
"""
            )

            explanation = response.text

            return {

                "attack":
                "Suspicious Message",

                "risk":
                "MEDIUM",

                "confidence":
                65,

                "grade":
                "B",

                "evidence":
                [],

                "explanation":
                explanation

            }

        except Exception:

            # ----------------------------------
            # FINAL SAFETY FALLBACK
            # ----------------------------------

            return {

                "attack":
                "Message Review Required",

                "risk":
                "MEDIUM",

                "confidence":
                50,

                "grade":
                "B",

                "evidence":
                [],

                "explanation":
                "The AI service was temporarily unavailable. The message could not be fully analyzed, but caution is recommended when dealing with unknown links, requests for money, passwords, OTPs, or personal information."

            }