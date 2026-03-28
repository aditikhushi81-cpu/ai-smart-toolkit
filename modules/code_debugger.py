def debug_code(code):
    if "==" in code and "=" in code:
        return "⚠️ Check assignment vs comparison operators"

    if "print" not in code:
        return "⚠️ Missing print statement"

    return "✅ Code looks fine (basic check)"