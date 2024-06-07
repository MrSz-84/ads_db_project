-- TABLES SECTION --

-- Creates miesiace table, containing Polish month names.
CREATE TABLE IF NOT EXISTS "miesiace" (
    "id" INTEGER,
    "miesiac" TEXT NOT NULL UNIQUE CHECK(
        "miesiac" IN (
            'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj',
            'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
            'Październik', 'Listopad', 'Grudzień'
        )
    ),
    PRIMARY KEY("id")
);

-- Creates dni_tyg table, containing Polish names for dows.
CREATE TABLE IF NOT EXISTS "dni_tyg" (
    "id" INTEGER,
    "dzien_tyg" TEXT NOT NULL UNIQUE CHECK(
        "dzien_tyg" IN (
            'Poniedziałek', 'Wtorek', 'Środa', 
            'Czwartek', 'Piątek', 'Sobota', 'Niedziela'
        )
    ),
    PRIMARY KEY("id")
);

-- Creates data_czas table, containing date related data. Time data is absent at this point.
CREATE TABLE IF NOT EXISTS "data_czas" (
    "id" INTEGER,
    "data" TEXT NOT NULL UNIQUE,
    "dzien" INTEGER CHECK("dzien" BETWEEN 1 AND 31),
    "dzien_tyg_nr" INTEGER CHECK("dzien_tyg_nr" BETWEEN 1 AND 7),
    "tydzien" INTEGER CHECK("tydzien" BETWEEN 0 AND 53),
    "miesiac_nr" INTEGER CHECK("miesiac_nr" BETWEEN 1 AND 12),
    "rok" INTEGER CHECK("rok" BETWEEN 1900 AND 9999),
    PRIMARY KEY("id"),
    FOREIGN KEY("dzien_tyg_nr") REFERENCES "dni_tyg"("id"),
    FOREIGN KEY("miesiac_nr") REFERENCES "miesiace"("id")
);

-- Creates wydawcy table, containing publisher names.
CREATE TABLE IF NOT EXISTS "wydawcy" (
    "id" INTEGER,
    "wydawca" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- Creates formaty table, contaning display format names.
CREATE TABLE IF NOT EXISTS "formaty" (
    "id" INTEGER,
    "format" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- Creates brandy table, contaning names of the brands instructing advertisements.
CREATE TABLE IF NOT EXISTS "brandy" (
    "id" INTEGER,
    "brand" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- Creates urzadzenie table, contaning types of device on which ad is being displayed.
CREATE TABLE IF NOT EXISTS "urzadzenia" (
    "id" INTEGER,
    "urzadzenie" TEXT NOT NULL UNIQUE CHECK(
        "urzadzenie" IN (
            'D', 'M', 'C'
            )
        ),
    PRIMARY KEY("id")
);

-- Creates main table placementy, containing unique display placement recorded on emissions for every analysed brand.
CREATE TABLE IF NOT EXISTS "placementy" (
    "id" INTEGER,
    "data" TEXT NOT NULL,
    "wydawca_id" INTEGER NOT NULL,
    "format_id" INTEGER NOT NULL,
    "urzadzenie_id" INTEGER NOT NULL,
    "brand_id" INTEGER NOT NULL,
    "pv" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("wydawca_id") REFERENCES "wydawcy"("id"),
    FOREIGN KEY("format_id") REFERENCES "formaty"("id"),
    FOREIGN KEY("urzadzenie_id") REFERENCES "urzadzenia"("id"),
    FOREIGN KEY("brand_id") REFERENCES "brandy"("id")
);


-- PROCEDURES, FUNCTIONS, TRIGGER FUNCTIONS SECTION --

-- FUNCTIONS SECTION--

-- TRIGGERS SECTION --
-- Adds entry at dzien column, after population of data row.
CREATE TRIGGER IF NOT EXISTS "dodaj_dzien"
AFTER INSERT ON "data_czas"
FOR EACH ROW
BEGIN
    UPDATE "data_czas"
    SET "dzien" =  CASE
        WHEN NEW."dzien" IS NULL THEN CAST(strftime('%d', NEW."data") AS INTEGER)
        ELSE NEW."dzien"
    END
    WHERE "id" = NEW."id";
END;

-- Adds entry at dzien_tyg_nr column, after population of data row.
CREATE TRIGGER IF NOT EXISTS "dodaj_dzien_tyg"
AFTER INSERT ON "data_czas"
FOR EACH ROW
BEGIN
    UPDATE "data_czas"
    SET "dzien_tyg_nr" = CASE 
        WHEN NEW."dzien_tyg_nr" IS NULL THEN
            CASE 
                WHEN CAST(strftime('%w', NEW."data") AS INTEGER) = 0 THEN 7
                ELSE CAST(strftime('%w', NEW."data") AS INTEGER)
            END
        ELSE NEW."dzien_tyg_nr"
    END
    WHERE "id" = NEW."id";
END;

-- Adds entry at tydzien column, after population of data row.
CREATE TRIGGER IF NOT EXISTS "dodaj_tydzien"
AFTER INSERT ON "data_czas"
FOR EACH ROW
BEGIN
    UPDATE "data_czas"
    SET "tydzien" =  CASE
        WHEN NEW."tydzien" IS NULL THEN CAST(strftime('%W', NEW."data") AS INTEGER)
        ELSE NEW."tydzien"
    END
    WHERE "id" = NEW."id";
END;

-- Adds entry at miesiac_nr column, after population of data row.
CREATE TRIGGER IF NOT EXISTS "dodaj_miesiac"
AFTER INSERT ON "data_czas"
FOR EACH ROW
BEGIN
    UPDATE "data_czas" 
    SET "miesiac_nr" = CASE
        WHEN NEW."miesiac_nr" IS NULL THEN CAST(strftime('%m', NEW."data") AS INTEGER)
        ELSE NEW."miesiac_nr"
    END
    WHERE "id" = NEW."id";
END;

-- Adds entry at rok column, after population of data row.
CREATE TRIGGER IF NOT EXISTS "dodaj_rok"
AFTER INSERT ON "data_czas"
FOR EACH ROW
BEGIN
    UPDATE "data_czas" 
    SET "rok" = CASE
        WHEN NEW."rok" IS NULL THEN CAST(strftime('%Y', NEW."data") AS INTEGER)
        ELSE NEW."rok"
    END
    WHERE "id" = NEW."id";
END;



-- POPULATE SOME TABLES ON CREATION --
-- Add month names
INSERT INTO "miesiace" ("miesiac") VALUES
('Styczeń'), ('Luty'), ('Marzec'), ('Kwiecień'), ('Maj'),
('Czerwiec'), ('Lipiec'), ('Sierpień'), ('Wrzesień'),
('Październik'), ('Listopad'), ('Grudzień');


-- Add day of week 
INSERT INTO "dni_tyg" ("dzien_tyg") VALUES
('Poniedziałek'), ('Wtorek'), ('Środa'), 
('Czwartek'), ('Piątek'), ('Sobota'), ('Niedziela');

-- Add device 
INSERT INTO "urzadzenia" ("urzadzenie") VALUES
('D'), ('M'), ('C');