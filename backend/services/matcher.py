from .gemini import call_gemini, parse_json_response
from .github import fetch_good_first_issues
import json

RANK_REPOS_PROMPT = """
You are matching a developer to open source repositories where they will most 
likely make a successful first contribution.

USER PROFILE:
{profile}

CANDIDATE REPOSITORIES:
{repos}

Each repo has: name, url, description, stars, language, topics, open_issues, 
pushed_at, has_contributing, health_score.

TASK:
Rank these repos best to worst fit for THIS specific user.
Return the top 5 only.
Consider: skill level match, goal alignment, domain interest, activity level, 
welcoming signals (has_contributing, health_score).
Heavily penalize repos with very low health_score or no has_contributing for beginner users.

Return ONLY a JSON array, no extra text:
[
  {{
    "name": "owner/repo",
    "url": "https://github.com/owner/repo",
    "match_reason": "One sentence why this fits this specific user."
  }}
]
"""

PICK_ISSUE_PROMPT = """
You are helping a developer find exactly where to start contributing to a GitHub repo.

USER PROFILE:
{profile}

REPOSITORY: {repo_name}
REPOSITORY DESCRIPTION: {repo_description}

OPEN GOOD FIRST ISSUES:
{issues}

TASK:
Pick the single most approachable issue for this specific user.
Explain in plain English exactly what they would need to do to close it.
Be specific — mention the file type, the kind of change, what they need to understand first.
If no issues are a good fit, say so honestly.

Return ONLY this JSON, no extra text:
{{
  "issue_title": "...",
  "issue_url": "...",
  "what_to_do": "2-3 sentences: exactly what change to make and what to understand first.",
  "difficulty": "easy | moderate | hard",
  "no_good_fit": false
}}
"""

def hard_filter(repos: list, profile: dict) -> list:
    filtered = []
    for repo in repos:
        # Must have some health signal
        if repo["health_score"] < 20:
            continue
        # Must have been active recently
        if not repo["pushed_at"]:
            continue
        # Beginner users need contributing guide
        if profile["skill_level"] == "beginner" and not repo["has_contributing"]:
            continue
        filtered.append(repo)
    return filtered

def rank_repos(repos: list, profile: dict) -> list:
    prompt = RANK_REPOS_PROMPT.format(
        profile=json.dumps(profile, indent=2),
        repos=json.dumps(repos, indent=2)
    )
    response = call_gemini(prompt)
    return parse_json_response(response)

def explain_issues(top_repos: list, profile: dict) -> list:
    results = []
    for repo in top_repos:
        issues = fetch_good_first_issues(repo["name"])
        
        if not issues:
            results.append({
                **repo,
                "issue_title": None,
                "issue_url": None,
                "what_to_do": "No good first issues found right now. Watch this repo and check back soon.",
                "difficulty": None
            })
            continue

        prompt = PICK_ISSUE_PROMPT.format(
            profile=json.dumps(profile, indent=2),
            repo_name=repo["name"],
            repo_description=repo.get("description", ""),
            issues=json.dumps(issues, indent=2)
        )

        try:
            response = call_gemini(prompt)
            issue_data = parse_json_response(response)
            results.append({**repo, **issue_data})
        except Exception:
            results.append({**repo, "issue_title": None, "what_to_do": "Could not analyze issues."})

    return results

def run_matching(repos: list, profile: dict) -> list:
    # Layer 1: hard filter
    filtered = hard_filter(repos, profile)
    if not filtered:
        return []

    # Layer 2: AI ranking — top 5
    top_repos = rank_repos(filtered[:30], profile)

    # Layer 3: issue explanation for each of top 5
    final = explain_issues(top_repos, profile)

    return final