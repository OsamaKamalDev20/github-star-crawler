# GitHub Stars Crawler

This project collects star counts for 100,000 public GitHub repositories
using GitHub's GraphQL API and stores daily snapshots in PostgreSQL.

## Design Choices
- GraphQL used for efficiency
- Immutable snapshot table for stars
- Minimal row updates
- Rate-limit aware crawling

## Scaling to 500M repositories
- Sharded crawling
- Message queues
- Object storage (S3)
- Partitioned tables
- Columnar formats

## Schema Evolution
New entities (issues, PRs, comments) would be stored as immutable tables
with foreign keys and timestamps to minimize updates.
