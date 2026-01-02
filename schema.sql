CREATE TABLE IF NOT EXISTS repositories (
    id SERIAL PRIMARY KEY,
    github_node_id TEXT UNIQUE NOT NULL,
    owner TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repo_star_snapshots (
    repo_id INTEGER REFERENCES repositories(id),
    stars INTEGER NOT NULL,
    collected_at DATE NOT NULL,
    PRIMARY KEY (repo_id, collected_at)
);
