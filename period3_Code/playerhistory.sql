CREATE TABLE IF NOT EXISTS player_history (
    history_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    game_id INTEGER,
    score REAL,
    date_played TEXT DEFAULT CURRENT_DATE,
    FOREIGN KEY (player_id)
        REFERENCES players (player_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (game_id)
        REFERENCES games (game_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);


INSERT INTO player_history (player_id, game_id, score)
    VALUES (4, 1, 800), (4, 2, 1900);


SELECT * FROM player_history;
