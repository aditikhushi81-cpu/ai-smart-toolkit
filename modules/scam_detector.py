def detect_scam(text):
    text = text.lower()

    score = 0
    reasons = []

    # 🚨 Urgency
    if any(word in text for word in ["urgent", "act now", "limited time", "now"]):
        score += 2
        reasons.append("Uses urgency language")

    # 💸 Money / prize
    if any(word in text for word in ["won", "prize", "lottery", "₹", "rs", "money"]):
        score += 3
        reasons.append("Too good to be true offer")

    # 🔗 Links
    if "http" in text or "www" in text:
        score += 3
        reasons.append("Contains suspicious link")

    # 🏦 Fake authority
    if any(word in text for word in ["bank", "account", "verify"]):
        score += 2
        reasons.append("Pretends to be official service")

    # 🎯 FINAL DECISION (UPDATED)
    if score >= 7:
        return {
            "Result": "❌ High Scam Risk",
            "Reason": ", ".join(reasons),
            "Confidence": "95%"
        }
    elif score >= 4:
        return {
            "Result": "⚠️ Medium Risk",
            "Reason": ", ".join(reasons),
            "Confidence": "75%"
        }
    else:
        return {
            "Result": "✅ Seems Safe",
            "Reason": "No strong scam indicators detected",
            "Confidence": "60%"
        }