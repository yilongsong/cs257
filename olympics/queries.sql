SELECT DISTINCT noc
FROM athletes
ORDER BY noc ASC;

SELECT DISTINCT name
FROM athletes
WHERE athletes.team='Kenya';

SELECT year, medal
FROM raw
WHERE name LIKE '%Greg%Louganis%' AND medal!='NA'
ORDER BY year ASC;

SELECT DISTINCT raw.noc, count(raw.medal)
FROM raw
GROUP BY raw.noc
ORDER BY count(raw.medal) DESC;