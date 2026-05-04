SELECT name, role, salary
FROM data/users.csv
WHERE department = 'Engineering' AND is_active = true
ORDER BY salary DESC