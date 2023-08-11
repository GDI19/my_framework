PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        name VARCHAR (32),
                        id_courses INTEGER [],
                        FOREIGN KEY (id_courses) REFERENCES course (id)
                        );

DROP TABLE IF EXISTS category;
CREATE TABLE category (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        name VARCHAR (32),
                        id_courses INTEGER [],
                        FOREIGN KEY (id_courses) REFERENCES course (id)
                        );

DROP TABLE IF EXISTS course;
CREATE TABLE course (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        name VARCHAR (32),
                        id_category INTEGER,
                        id_students INTEGER [],
                        FOREIGN KEY (id_category) REFERENCES category (id),
                        FOREIGN KEY (id_students) REFERENCES student (id)
                        );
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;