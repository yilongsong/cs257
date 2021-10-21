CREATE TABLE athletes (
    id INT,
    name TEXT,
    sex CHAR(1),
    age INT,
    height INT,
    weight float,
    noc_id INT,
    PRIMARY KEY (id)
);

CREATE TABLE noc_regions (
    id INT,
    noc CHAR(3),
    region TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE events (
    id INT GENERATED ALWAYS AS IDENTITY,
    games TEXT,
    year INT,
    season TEXT,
    city TEXT,
    sport TEXT,
    event TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE athlete_event (
    id INT,
    athlete_id INT,
    event_id INT,
    medal TEXT,
    PRIMARY KEY (id)
);