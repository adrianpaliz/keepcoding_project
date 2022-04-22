CREATE TABLE "movements" (
	"id"	INTEGER,
	"day"	TEXT NOT NULL,
	"hour"	TEXT NOT NULL,
	"currency_from"	TEXT NOT NULL,
	"amount_from"	REAL NOT NULL,
	"currency_to"	TEXT NOT NULL,
	"amount_to"	REAL NOT NULL,
	"unit_price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);