CREATE TABLE Rooms(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(40),
    type VARCHAR(40),

    PRIMARY KEY(id)
)
ENGINE = INNODB;
CREATE INDEX name ON Rooms(name);


CREATE TABLE Profils(
    id INTEGER NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    sexe VARCHAR(1),
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


CREATE TABLE Inhabitants(
    id INTEGER NOT NULL AUTO_INCREMENT,
    fk_profil_id INTEGER,

    PRIMARY KEY(id)
)
ENGINE = INNODB;

CREATE TABLE Guests(
    id INTEGER NOT NULL AUTO_INCREMENT,
    fk_profil_id INTEGER,

    PRIMARY KEY(id)
)
ENGINE = INNODB;

ALTER TABLE Events
ADD FOREIGN KEY(fk_room_id) REFERENCES Rooms(id);

ALTER TABLE Inhabitants
ADD FOREIGN KEY(fk_profil_id) REFERENCES Profils(id);

ALTER TABLE Guests
ADD FOREIGN KEY(fk_profil_id) REFERENCES Profils(id);