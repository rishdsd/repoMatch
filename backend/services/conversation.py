STAGES = [
    {
        "id": "language",
        "question": "What language or stack do you spend most of your time in?",
        "type": "text",
        "hint": "e.g. Python, JavaScript, Go, Rust..."
    },
    {
        "id": "can_read_code",
        "question": "Have you ever read someone else's codebase and made meaningful changes to it?",
        "type": "quick_reply",
        "options": [
            "Yes, comfortably",
            "Yes but it took a while",
            "Not really"
        ]
    },
    {
        "id": "goal",
        "question": "What is driving you to contribute right now?",
        "type": "quick_reply",
        "options": [
            "I want a merged PR for my portfolio",
            "I want to learn something new",
            "I use a tool and want to improve it",
            "I want to become a regular contributor"
        ]
    },
    {
        "id": "domain",
        "question": "What kind of software do you genuinely find interesting?",
        "type": "quick_reply",
        "options": [
            "Dev tools / CLI",
            "Web / APIs",
            "Data / ML",
            "Infra / DevOps",
            "Mobile",
            "No preference"
        ]
    },
    {
        "id": "time",
        "question": "How much time can you put into this per week?",
        "type": "quick_reply",
        "options": [
            "Less than 2 hours",
            "2 to 5 hours",
            "More than 5 hours"
        ]
    },
    {
        "id": "first_time",
        "question": "Have you contributed to open source before?",
        "type": "quick_reply",
        "options": [
            "Yes, a few times",
            "Once or twice",
            "Never"
        ]
    }
]

def get_next_stage(answers: dict) -> dict | None:
    for stage in STAGES:
        if stage["id"] not in answers:
            return stage
    return None  # All stages complete

def is_complete(answers: dict) -> bool:
    return all(s["id"] in answers for s in STAGES)