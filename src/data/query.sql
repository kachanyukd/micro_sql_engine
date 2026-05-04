SELECT name, role, salary
FROM users.csv
WHERE department = 'Engineering' AND is_active = true
ORDER BY salary DESC