import tomli as tomllib
import dlt
import requests


with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

GITHUB_TOKEN = secrets["github"]["token"]

# GITHUB_TOKEN = "ghp_yourtoken"
GRAPHQL_URL = "https://api.github.com/graphql"

QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    issues(first: 100, after: $cursor, states: [OPEN, CLOSED]) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        title
        state
        createdAt
        closedAt
        author { login }
        labels(first: 10) {
          nodes { name }
        }
      }
    }
  }
}
"""

@dlt.resource(write_disposition="replace")
def github_issues_graphql(repo: str = "dlt-hub/dlt"):
    owner, name = repo.split("/")
    cursor = None
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    while True:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": QUERY, "variables": {"owner": owner, "name": name, "cursor": cursor}},
            headers=headers,
            timeout=30
        )
        data = response.json()
        issues = data["data"]["repository"]["issues"]

        for issue in issues["nodes"]:
            yield {
                "repo": repo,
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "author": issue["author"]["login"] if issue["author"] else None,
                "created_at": issue["createdAt"],
                "closed_at": issue["closedAt"],
                "labels": [l["name"] for l in issue["labels"]["nodes"]]
            }

        if not issues["pageInfo"]["hasNextPage"]:
            break
        cursor = issues["pageInfo"]["endCursor"]

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="github_lab",
        destination="postgres",
        dataset_name="raw",
    )
    info = pipeline.run([
        github_issues_graphql(repo="dlt-hub/dlt"),
        github_issues_graphql(repo="apache/superset"),
    ])
    print(info)