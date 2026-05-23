import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def build_search_query(profile: dict) -> str:
    parts = [
        f"language:{profile['language']}",
        "archived:false",
        "is:public",
        f"pushed:>{(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')}",
        "good-first-issues:>0",  # only repos with open good first issues
    ]

    if profile["skill_level"] == "beginner":
        parts.append("stars:50..800")
    else:
        parts.append("stars:50..5000")

    topics = profile.get("domain_topics", [])
    if topics:
        parts.append(f"topic:{topics[0]}")

    return " ".join(parts)

def search_repos(profile: dict, max_results: int = 30) -> list:
    query = build_search_query(profile)
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "updated",
        "order": "desc",
        "per_page": max_results
    }

    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json().get("items", [])

def fetch_community_profile(full_name: str) -> dict:
    url = f"https://api.github.com/repos/{full_name}/community/profile"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return {}

def fetch_good_first_issues(full_name: str) -> list:
    url = f"https://api.github.com/repos/{full_name}/issues"
    params = {
        "labels": "good first issue",
        "state": "open",
        "per_page": 5,
        "sort": "created",
        "direction": "desc"
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    if resp.status_code == 200:
        issues = resp.json()
        return [
            {
                "number": i["number"],
                "title": i["title"],
                "url": i["html_url"],
                "body_preview": (i.get("body") or "")[:300],
                "comments": i["comments"],
                "created_at": i["created_at"]
            }
            for i in issues if "pull_request" not in i
        ]
    return []

def enrich_repos(repos: list) -> list:
    """Fetch community profiles in parallel for all repos."""
    enriched = []

    def process(repo):
        profile = fetch_community_profile(repo["full_name"])
        return {
            "name": repo["full_name"],
            "url": repo["html_url"],
            "description": repo.get("description") or "",
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo.get("language") or "",
            "topics": repo.get("topics") or [],
            "open_issues": repo["open_issues_count"],
            "pushed_at": repo["pushed_at"],
            "license": (repo.get("license") or {}).get("name"),
            "has_contributing": profile.get("files", {}).get("contributing") is not None,
            "has_code_of_conduct": profile.get("files", {}).get("code_of_conduct") is not None,
            "health_score": profile.get("health_percentage", 0),
        }

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process, repo): repo for repo in repos}
        for future in as_completed(futures):
            try:
                enriched.append(future.result())
            except Exception:
                pass

    return enriched