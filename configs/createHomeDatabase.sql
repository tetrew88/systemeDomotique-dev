CREATE TABLE Rooms(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(40),
    type VARCHAR(40),

    PRIMARY KEY(id)
)
ENGINE = INNODB;
CREATE INDEX name ON Rooms(name);
CREATE INDEX type ON Rooms(type);


CREATE TABLE Profils(
    id INTEGER NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    gender VARCHAR(1),
    date_of_birth VARCHAR(15),

    PRIMARY KEY(id)
)
ENGINE = INNODB;
CREATE INDEX first_name ON Profils(first_name);
CREATE INDEX last_name ON Profils(last_name);


CREATE TABLE Events(
    id INTEGER NOT NULL AUTO_INCREMENT,
    type VARCHAR(40),
    datetime VARCHAR(60),
    fk_room_id INTEGER,

    PRIMARY KEY(id)
)
ENGINE = INNODB;
CREATE INDEX type ON Events(type);
CREATE INDEX datetime ON Events(datetime);
CREATE INDEX fk_room_id ON Events(fk_room_id);


CREATE TABLE Users(
    id INTEGER NOT NULL AUTO_INCREMENT,
    fk_profil_id INTEGER,
    grade VARCHAR(40),
    role VARCHAR(40),
    identifiant VARCHAR(40),
    password VARCHAR(40),

    PRIMARY KEY(id)
)
ENGINE = INNODB;
CREATE INDEX fk_profil_id ON Users(fk_profil_id);
CREATE INDEX grade ON Users(grade);
CREATE INDEX role ON Users(role);
CREATE INDEX identifiant ON Users(identifiant);

ALTER TABLE Events
ADD FOREIGN KEY(fk_room_id) REFERENCES Rooms(id);

ALTER TABLE Users
ADD FOREIGN KEY(fk_profil_id) REFERENCES Profils(id);
