from fastapi import APIRouter
from pydantic import BaseModel
from ..services.conversation import get_next_stage, is_complete
from ..services.profile import build_profile
from ..services.github import search_repos, enrich_repos
from ..services.matcher import run_matching

router = APIRouter()

class ChatMessage(BaseModel):
    answers: dict          # All answers collected so far
    latest_answer: str     # The answer just submitted
    latest_stage_id: str   # Which stage was just answered

@router.post("/chat")
async def chat(payload: ChatMessage):
    # Record the latest answer
    answers = payload.answers
    answers[payload.latest_stage_id] = payload.latest_answer

    if is_complete(answers):
        profile = build_profile(answers)
        print("\n=== PROFILE ===")
        print(profile)

        repos = search_repos(profile)
        print(f"\n=== RAW REPOS: {len(repos)} ===")
        for r in repos[:3]:  # print first 3 only
            print(f"  - {r['full_name']} | stars: {r['stargazers_count']}")

        enriched = enrich_repos(repos)
        print(f"\n=== ENRICHED: {len(enriched)} ===")
        for r in enriched[:3]:
            print(f"  - {r['name']} | health: {r['health_score']} | contributing: {r['has_contributing']}")

        results = run_matching(enriched, profile)
        print(f"\n=== FINAL RESULTS: {len(results)} ===")
        for r in results:
            print(f"  - {r.get('name')} | issue: {r.get('issue_title')} | url: {r.get('url')}")
        print("================\n")

    # Not complete — return next question
    next_stage = get_next_stage(answers)
    return {
        "status": "continue",
        "next_stage": next_stage,
        "answers": answers
    }