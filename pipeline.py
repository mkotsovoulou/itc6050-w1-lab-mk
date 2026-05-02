import dlt
import requests

@dlt.resource(write_disposition="replace")
def github_issues(repo: str = "dlt-hub/dlt"):
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {"state": "all", "per_page": 100, "page": 1}

    while True:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        page = response.json()
        if not page:
            break
        for item in page:
            if "pull_request" not in item:
                item["repo"] = repo   # ← add repo column
                yield item
        params["page"] += 1
        if params["page"] > 5:
            break

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_lab",
        destination="postgres",
        dataset_name="raw",
    )
    # Run both repos
    info = pipeline.run([
        github_issues(repo="dlt-hub/dlt"),
        github_issues(repo="apache/superset"),
    ])
    print(info)