CREATE TABLE "movements" (
	"id"	INTEGER,
	"day"	TEXT NOT NULL,
	"hour"	TEXT NOT NULL,
	"currency_from"	TEXT NOT NULL,
	"amount_from_hidden"	REAL NOT NULL,
	"currency_to"	TEXT NOT NULL,
	"amount_to_hidden"	REAL NOT NULL,
	"unit_price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);