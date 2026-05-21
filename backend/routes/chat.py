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

    # Check if conversation is complete
    if is_complete(answers):
        profile = build_profile(answers)
        
        # DEBUG
        from ..services.github import build_search_query, search_repos, enrich_repos
        query = build_search_query(profile)
        print("SEARCH QUERY:", query)
        
        repos = search_repos(profile)
        print("RAW REPOS COUNT:", len(repos))
        
        enriched = enrich_repos(repos)
        print("ENRICHED COUNT:", len(enriched))
        
        results = run_matching(enriched, profile)
        print("FINAL RESULTS:", len(results))

        return {
            "status": "complete",
            "results": results
        }

    # Not complete — return next question
    next_stage = get_next_stage(answers)
    return {
        "status": "continue",
        "next_stage": next_stage,
        "answers": answers
    }