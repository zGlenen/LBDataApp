CREATE TABLE "genre" (
    "id"    INTEGER NOT NULL PRIMARY KEY,
    "name"  TEXT NOT NULL
);

CREATE TABLE "film_genre" (
    "film_id"   INTEGER NOT NULL,
    "genre_id"  INTEGER NOT NULL,
    PRIMARY KEY("film_id", "genre_id"),
    FOREIGN KEY("film_id") REFERENCES "film"("film_id"),
    FOREIGN KEY("genre_id") REFERENCES "genre"("id")
);

CREATE TABLE "film" (
    "film_id"       INTEGER NOT NULL PRIMARY KEY,
    "title"         TEXT NOT NULL,
    "release_year"  INTEGER NOT NULL,
    "letterboxd_url" TEXT,
    "date_added"    TEXT,
    FOREIGN KEY("film_id") REFERENCES "film_genre"("film_id")
);

CREATE TABLE "film_country" (
	"fim_id"	INTEGER NOT NULL,
	"country"	TEXT NOT NULL,
	FOREIGN KEY("fim_id") REFERENCES "film"("film_id"),
	PRIMARY KEY("fim_id")
)