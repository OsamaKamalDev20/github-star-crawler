import requests
import time

GITHUB_API_URL = "https://api.github.com/graphql"

class GitHubClient:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def fetch_repositories(self, cursor=None):
        query = """
        query ($cursor: String) {
          search(query: "stars:>0", type: REPOSITORY, first: 100, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              ... on Repository {
                id
                name
                owner {
                  login
                }
                stargazerCount
              }
            }
          }
          rateLimit {
            remaining
            resetAt
          }
        }
        """

        response = requests.post(
            GITHUB_API_URL,
            json={"query": query, "variables": {"cursor": cursor}},
            headers=self.headers,
        )

        if response.status_code != 200:
            raise Exception("GitHub API error")

        data = response.json()

        rate = data["data"]["rateLimit"]
        if rate["remaining"] < 50:
            print("Rate limit low, sleeping...")
            time.sleep(10)

        return data["data"]
