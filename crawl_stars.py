import os
import psycopg2
from github_client import GitHubClient
from db import Database

MAX_REPOS = 100_000

def main():
    token = os.environ["GITHUB_TOKEN"]

    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="postgres"
    )

    db = Database(conn)
    gh = GitHubClient(token)

    cursor = None
    count = 0

    while count < MAX_REPOS:
        data = gh.fetch_repositories(cursor)
        repos = data["search"]["nodes"]

        for repo in repos:
            repo_id = db.insert_repository(
                repo["id"],
                repo["owner"]["login"],
                repo["name"]
            )
            db.insert_star_snapshot(repo_id, repo["stargazerCount"])
            count += 1

            if count >= MAX_REPOS:
                break

        cursor = data["search"]["pageInfo"]["endCursor"]
        print(f"Collected {count} repositories")

if __name__ == "__main__":
    main()
