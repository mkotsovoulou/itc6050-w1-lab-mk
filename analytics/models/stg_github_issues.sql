-- models/stg_github_issues.sql
SELECT
    id          AS issue_id,
    number      AS issue_number,
    title,
    state,
    repo,
    user__login AS author,
    created_at,
    closed_at,
    EXTRACT(DAY FROM (COALESCE(closed_at, NOW()) - created_at)) AS days_open
FROM {{ source('raw', 'github_issues') }}