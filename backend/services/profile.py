def build_profile(answers: dict) -> dict:
    
    # Map can_read_code answer to skill level
    skill_map = {
        "Yes, comfortably": "intermediate",
        "Yes but it took a while": "beginner",
        "Not really": "beginner"
    }

    # Map domain answer to GitHub topic keywords
    domain_topic_map = {
        "Dev tools / CLI": ["cli", "devtools", "developer-tools", "terminal"],
        "Web / APIs": ["web", "api", "rest", "http", "framework"],
        "Data / ML": ["machine-learning", "data", "deep-learning", "nlp", "pytorch"],
        "Infra / DevOps": ["devops", "kubernetes", "docker", "infrastructure", "cloud"],
        "Mobile": ["mobile", "android", "ios", "react-native", "flutter"],
        "No preference": []
    }

    # Map time to complexity tolerance
    time_map = {
        "Less than 2 hours": "low",
        "2 to 5 hours": "medium",
        "More than 5 hours": "high"
    }

    return {
        "language": answers.get("language", "").strip(),
        "skill_level": skill_map.get(answers.get("can_read_code"), "beginner"),
        "goal": answers.get("goal"),
        "domain": answers.get("domain"),
        "domain_topics": domain_topic_map.get(answers.get("domain"), []),
        "time_available": answers.get("time"),
        "complexity_tolerance": time_map.get(answers.get("time"), "low"),
        "first_time": answers.get("first_time") == "Never",
        "prior_contributions": answers.get("first_time")
    }