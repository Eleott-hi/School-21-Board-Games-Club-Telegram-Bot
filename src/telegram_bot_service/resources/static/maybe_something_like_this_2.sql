CREATE TABLE GameDescription (
    id SERIAL PRIMARY KEY,
    gameName VARCHAR(255),
    year INT,
    gameShortDescription TEXT,
    gameFullDescription TEXT,
    coverImageLink VARCHAR(255),
    videoRulesLink VARCHAR(255),
    genre_id INT,
    status_id INT,
    status_date DATE,
    FOREIGN KEY (genre_id) REFERENCES Genres(id),
    FOREIGN KEY (status_id) REFERENCES Statuses(id)
);

-- GameRestrictions table
CREATE TABLE GameRestrictions (
    id SERIAL PRIMARY KEY,
    game_id INT,
    minPlayers INT,
    maxPlayers INT,
    minIdealPlayers INT,
    maxIdealPlayers INT,
    minPlayTime INT,
    maxPlayTime INT,
    minAge INT,
    FOREIGN KEY (game_id) REFERENCES GameDescription(id)
);

-- Owners table
CREATE TABLE Owners (
    id SERIAL PRIMARY KEY,
    owner_name VARCHAR(255) NOT NULL
);

-- Genres table
CREATE TABLE Genres (
    id SERIAL PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL
);

-- Statuses table
CREATE TABLE Statuses (
    id SERIAL PRIMARY KEY,
    status_name VARCHAR(255) NOT NULL
);

INSERT INTO Statuses (status_name) VALUES ('В школе');
INSERT INTO Statuses (status_name) VALUES ('Забронирована');
INSERT INTO Statuses (status_name) VALUES ('Забрал(а) поиграть');

-- Sample data for Genres (you can add more genres as needed)
INSERT INTO Genres (genre_name) VALUES ('Азартные');
INSERT INTO Genres (genre_name) VALUES ('Война');
INSERT INTO Genres (genre_name) VALUES ('Карты');
INSERT INTO Genres (genre_name) VALUES ('Классика');
INSERT INTO Genres (genre_name) VALUES ('Компанейские');
INSERT INTO Genres (genre_name) VALUES ('Логические');
INSERT INTO Genres (genre_name) VALUES ('Приключения');
INSERT INTO Genres (genre_name) VALUES ('Экономика');

CREATE OR REPLACE FUNCTION add_new_game(
  p_gameName VARCHAR,
  p_year INT,
  p_gameShortDescription TEXT,
  p_gameFullDescription TEXT,
  p_coverImageLink VARCHAR,
  p_videoRulesLink VARCHAR,
  p_genre_id INT,
  p_status_id INT,
  p_status_date DATE,
  p_minPlayers INT,
  p_maxPlayers INT,
  p_minIdealPlayers INT,
  p_maxIdealPlayers INT,
  p_minPlayTime INT,
  p_maxPlayTime INT,
  p_minAge INT
) RETURNS VOID AS $$
DECLARE
  v_game_id INT;
BEGIN
  INSERT INTO GameDescription (
    gameName,
    year,
    gameShortDescription,
    gameFullDescription,
    coverImageLink,
    videoRulesLink,
    genre_id,
    status_id,
    status_date
  ) VALUES (
    p_gameName,
    p_year,
    p_gameShortDescription,
    p_gameFullDescription,
    p_coverImageLink,
    p_videoRulesLink,
    p_genre_id,
    p_status_id,
    p_status_date
  ) RETURNING id INTO v_game_id;

  INSERT INTO GameRestrictions (
    game_id,
    minPlayers,
    maxPlayers,
    minIdealPlayers,
    maxIdealPlayers,
    minPlayTime,
    maxPlayTime,
    minAge
  ) VALUES (
    v_game_id,
    p_minPlayers,
    p_maxPlayers,
    p_minIdealPlayers,
    p_maxIdealPlayers,
    p_minPlayTime,
    p_maxPlayTime,
    p_minAge
  );
END;
$$ LANGUAGE plpgsql;