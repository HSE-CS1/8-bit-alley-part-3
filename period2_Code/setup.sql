-- we need to create a database table

-- some setup for sqlite
.mode box
.open gamers.db

-- let's delete the table first, then re-create it
DROP TABLE IF EXISTS players;

-- make the players table
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE,
    join_date TEXT DEFAULT CURRENT_DATE,
    verified TEXT
);


-- add some data or rows to our players table
INSERT INTO players (username, email)
    VALUES ('PixelMaster', 'pixel@email.com'),
           ('JoystickJunkie', 'jj@email.com'),
           ('RetroQueen', 'queen@email.com'),
           ('ControllerChuck', 'cc@email.net'),
           ('bit_Hacker', 'admin@bit_hacker.org');
-- add one with a join date
INSERT INTO players (username, email, join_date)
    VALUES ('CyberKnight', 'knight@shell.org', '2026-02-05');

-- let's see what is in our table
SELECT * FROM players;

-- let's add a second table for the games at the arcade
DROP TABLE IF EXISTS games;

CREATE TABLE IF NOT EXISTS games(
    game_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    released_year INTEGER,
    price_per_play REAL CHECK(price_per_play >= 0)
);

-- add some data to the games table
INSERT INTO games (title, genre, released_year, price_per_play)
    VALUES
        ('Glactic Defender', 'Shooter', 1982, 0.25),
        ('Neon Racer', 'Racing', 1995, 0.50),
        ('Labyrinth', 'Puzzle', 1988, 0.25);

-- show the data
SELECT * FROM games;





