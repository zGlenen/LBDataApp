-- Drop existing tables if they exist
DROP TABLE IF EXISTS "film_person_crew";
DROP TABLE IF EXISTS "film_person_cast";
DROP TABLE IF EXISTS "person";
DROP TABLE IF EXISTS "film_country";
DROP TABLE IF EXISTS "film_genre";
DROP TABLE IF EXISTS "film_common";
DROP TABLE IF EXISTS "genre";

-- Create new tables
CREATE TABLE "genre" (
    "id"    INTEGER NOT NULL PRIMARY KEY,
    "name"  TEXT NOT NULL
);

CREATE TABLE "film" (
    "id"       INTEGER NOT NULL PRIMARY KEY,
    "title"         TEXT NOT NULL,
    "release_year"  INTEGER NOT NULL,
    "date_added"    TEXT,
    "letterboxd_url" TEXT,
    "runtime"       INTEGER NOT NULL
);


CREATE TABLE "film_genre" (
    "film_id"   INTEGER NOT NULL,
    "genre_id"  INTEGER NOT NULL,
    PRIMARY KEY("film_id", "genre_id"),
    FOREIGN KEY("film_id") REFERENCES "film"("id"),
    FOREIGN KEY("genre_id") REFERENCES "genre"("id")
);

-- Continue creating other tables step by step
CREATE TABLE "film_country" (
	"film_id"	INTEGER NOT NULL,
	"country"	TEXT NOT NULL,
	FOREIGN KEY("film_id") REFERENCES "film"("id")
);

CREATE TABLE "person" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);


CREATE TABLE "film_person_cast" (
    "film_id"   INTEGER,
    "person_id" INTEGER,
    "character" TEXT NOT NULL,
    FOREIGN KEY("film_id") REFERENCES "film"("id"),
    FOREIGN KEY("person_id") REFERENCES "person"("id"),
    PRIMARY KEY("film_id", "person_id")
);

CREATE TABLE "film_person_crew" (
    "film_id" INTEGER,
    "person_id" INTEGER,
    "job" TEXT NOT NULL,
    FOREIGN KEY("film_id") REFERENCES "film"("id"),
    FOREIGN KEY("person_id") REFERENCES "person"("id"),
    PRIMARY KEY("film_id", "person_id")
);
