from google import genai
import json
import re

# ----------------------------------
# GEMINI CLIENT
# ----------------------------------

import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ----------------------------------
# CYBER INVESTIGATION ENGINE
# ----------------------------------

def investigate_message(message):

    prompt = f"""
You are an Expert Cyber Security Threat Analyst.

Analyze the following message.

Message:
{message}

Determine:

1. Attack Type
2. Risk Level
3. Confidence Score (0-100)
4. Explanation

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

Do not return markdown.
Do not return extra text.
Return only JSON.
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

        # Auto Grade Calculation

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
Analyze this message.

Message:
{message}

Explain whether it appears suspicious and why.
"""
            )

            explanation = response.text

            return {

                "attack":
                "AI Threat Analysis",

                "risk":
                "MEDIUM",

                "confidence":
                60,

                "grade":
                "B",

                "evidence":
                [],

                "explanation":
                explanation

            }

        except Exception as e:

            return {

                "attack":
                "Unable To Analyze",

                "risk":
                "LOW",

                "confidence":
                0,

                "grade":
                "A+",

                "evidence":
                [],

                "explanation":
                str(e)

            }