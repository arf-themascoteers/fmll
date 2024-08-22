SELECT objectId, COUNT(*) AS combination_count
FROM (
    SELECT objectId, networkid, timestamp
    FROM path
    GROUP BY objectId, networkid, timestamp
) AS subquery
GROUP BY objectId
HAVING COUNT(*) > 1;
