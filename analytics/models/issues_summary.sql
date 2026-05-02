WITH issues AS (
  SELECT * FROM {{ ref('stg_github_issues') }}
)
SELECT
  date_trunc('month', created_at)::date  AS month,
  state,
  COUNT(*)                                AS issue_count,
  ROUND(AVG(days_open)::numeric, 1)       AS avg_days_open
FROM issues
GROUP BY 1, 2
ORDER BY 1, 2