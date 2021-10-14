
CREATE TABLE athletes (
    id INT
    name TEXT,
    sex CHAR(1),
    age INT,
    height INT,
    weight float,
    team TEXT,
    noc CHAR(3)
    PRIMARY KEY (id)
);

CREATE TABLE events (
    id INT GENERATED ALWAYS AS IDENTITY,
    games TEXT,
    year INT,
    season TEXT,
    city TEXT,
    sport TEXT,
    event TEXT
);

CREATE TABLE raw (
    id INT GENERATED ALWAYS AS IDENTITY,
    athlete_id INT,
    name TEXT,
    sex CHAR(1),
    age INT,
    height INT,
    weight float,
    team TEXT,
    noc CHAR(3),
    games TEXT,
    year INT,
    season TEXT,
    city TEXT,
    sport TEXT,
    event TEXT,
    medal TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE athlete_events (
    id INT,
    athlete_id INT,
    event_id INT,
    medal TEXT
);

INSERT INTO athlete_events (id, athlete_id, event_id, medal)
SELECT raw.id, raw.athlete_id, events.id, raw.medal
FROM raw, athletes, events
WHERE events.games = raw.games AND events.year = raw.year
AND events.season = raw.season AND events.city = raw.city
AND events.sport = raw.sport AND events.event = raw.event;