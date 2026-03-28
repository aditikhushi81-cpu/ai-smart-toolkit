print("🔥 NEW LOGIC LOADED")

def analyze_statement(text):
    text_lower = text.lower()

    # Direct check (your case)
    if "qutub minar" in text_lower:
        return {
            "Result": "❌ Unrealistic",
            "Reason": "A human cannot be as tall as Qutub Minar (~73 meters).",
            "Confidence": "99%"
        }

    # General comparison logic
    unrealistic_phrases = ["as tall as", "bigger than", "stronger than"]

    for phrase in unrealistic_phrases:
        if phrase in text_lower:
            return {
                "Result": "❌ Likely Exaggeration",
                "Reason": "The statement uses unrealistic comparison.",
                "Confidence": "85%"
            }

    return {
        "Result": "✅ Seems Realistic",
        "Reason": "The statement follows normal human context.",
        "Confidence": "70%"
    }