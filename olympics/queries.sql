SELECT DISTINCT noc
FROM noc_regions
ORDER BY noc ASC;

SELECT DISTINCT name
FROM athletes, noc_regions
WHERE athletes.noc_id = noc_regions.id AND noc_regions.region='Kenya';

SELECT events.year, athlete_event.medal
FROM athletes, events, athlete_event
WHERE athlete_event.athlete_id = athletes.id AND athlete_event.event_id = events.id AND athletes.name LIKE '%Greg%Louganis%' AND athlete_event.medal!='NA'
ORDER BY year ASC;

SELECT noc_regions.noc, count(athlete_event.id)
FROM athletes, athlete_event, noc_regions
WHERE athlete_event.athlete_id = athletes.id AND athlete_event.medal='Gold' AND athletes.noc_id = noc_regions.id
GROUP BY noc_regions.noc
ORDER BY count(athlete_event.athlete_id) DESC;