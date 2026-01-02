import psycopg2
from datetime import date

class Database:
    def __init__(self, conn):
        self.conn = conn

    def insert_repository(self, node_id, owner, name):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO repositories (github_node_id, owner, name)
                VALUES (%s, %s, %s)
                ON CONFLICT (github_node_id) DO NOTHING
                RETURNING id
            """, (node_id, owner, name))
            result = cur.fetchone()
            self.conn.commit()

            if result:
                return result[0]

            cur.execute(
                "SELECT id FROM repositories WHERE github_node_id = %s",
                (node_id,)
            )
            return cur.fetchone()[0]

    def insert_star_snapshot(self, repo_id, stars):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO repo_star_snapshots (repo_id, stars, collected_at)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (repo_id, stars, date.today()))
            self.conn.commit()
