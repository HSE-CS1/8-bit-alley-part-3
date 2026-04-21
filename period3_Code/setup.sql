-- some sqlite settings
.mode box
.open gamers.db

-- let's delete the table
DROP TABLE IF EXISTS players;

-- let's create a player table
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE,
    join_date TEXT DEFAULT CURRENT_DATE,
    verified TEXT
);


-- let's add some data to our player table
INSERT INTO players (username, email)
    VALUES ('PixelMaster', 'pixel@email.com'),
           ('JoystickJunkie', 'jj@email.com'),
           ('RetroQueen', 'queen@email.com'),
           ('ControllerChuck', 'chuck@gamer.net'),
           ('bit_Hacker', 'admin@bit_hacker.org');

INSERT INTO players (username, email, join_date)
    VALUES ('CyberKnight', 'knight99@sample.org', '2026-02-12');


-- see the players table
SELECT * FROM players;

DROP TABLE IF EXISTS games;
-- let's add the games table
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    released_year INTEGER,
    price_per_play REAL CHECK(price_per_play >= 0)
);

-- add some games to the table
INSERT INTO games (title, genre, released_year, price_per_play)
    VALUES
        ('Galactic Defender', 'Shooter', 1982, 0.25),
        ('Neon Racer', 'Racing', 1995, 0.50),
        ('Labyrinth', 'Puzzle', 1988, 0.25),
        ('Dungeon Crawler', 'RPG', 1998, 0.50);

-- show the games data
SELECT * FROM games;

