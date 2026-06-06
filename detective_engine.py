attack_patterns = {

    "Phishing Scam": [
        "click the link",
        "verify account",
        "login now",
        "confirm account"
    ],

    "Fake Job Scam": [
        "registration fee",
        "pay fee",
        "interview fee",
        "job offer"
    ],

    "OTP Theft": [
        "share otp",
        "send otp",
        "verify otp"
    ],

    "Investment Scam": [
        "double your money",
        "guaranteed return",
        "earn lakhs",
        "investment opportunity"
    ],

    "Lottery Scam": [
        "you won",
        "claim reward",
        "congratulations",
        "winner"
    ],

    "Tech Support Scam": [
        "system infected",
        "virus detected",
        "call support",
        "security alert"
    ]
}


def investigate_message(text):

    text = text.lower()

    detected_attack = "Unknown"

    confidence = 0

    evidence = []

    for attack, patterns in attack_patterns.items():

        score = 0
        found_patterns = []

        for pattern in patterns:

            if pattern in text:

                score += 1
                found_patterns.append(pattern)

        if score > confidence:

            confidence = score
            detected_attack = attack
            evidence = found_patterns

    # -------------------------
    # THREAT SCORE
    # -------------------------

    threat_score = min(confidence * 25, 100)

    # -------------------------
    # RISK LEVEL
    # -------------------------

    if threat_score >= 75:
        risk = "CRITICAL"
        grade = "D"

    elif threat_score >= 50:
        risk = "HIGH"
        grade = "C"

    elif threat_score >= 25:
        risk = "MEDIUM"
        grade = "B"

    else:
        risk = "LOW"
        grade = "A+"

    # -------------------------
    # AI EXPLANATIONS
    # -------------------------

    explanations = {

        "Phishing Scam":
        "This message attempts to steal personal information by asking users to verify accounts or click suspicious links.",

        "Fake Job Scam":
        "This message uses fake job opportunities and requests money through registration or interview fees.",

        "OTP Theft":
        "The sender attempts to obtain OTP codes which can be used to access bank accounts or online services.",

        "Investment Scam":
        "The message promises unrealistic profits and guaranteed returns to attract victims.",

        "Lottery Scam":
        "The sender claims the victim has won a reward and uses excitement tactics to collect personal information or money.",

        "Tech Support Scam":
        "The attacker pretends to be technical support and creates fear to gain access to devices or personal data."
    }

    ai_explanation = explanations.get(
        detected_attack,
        "No major cyber threat detected. Continue to stay alert and verify unknown messages."
    )

    # -------------------------
    # RETURN RESULTS
    # -------------------------

    return {

        "attack": detected_attack,
        "confidence": threat_score,
        "risk": risk,
        "grade": grade,
        "evidence": evidence,
        "explanation": ai_explanation

    }