-- Удаление таблиц
DROP TABLE IF EXISTS "TestResult" CASCADE;
DROP TABLE IF EXISTS "TestCase" CASCADE;
DROP TABLE IF EXISTS "Solution" CASCADE;
DROP TABLE IF EXISTS "Task" CASCADE;
DROP TABLE IF EXISTS "UserHasSubject" CASCADE;
DROP TABLE IF EXISTS "Faculty" CASCADE;
DROP TABLE IF EXISTS "Group" CASCADE;
DROP TABLE IF EXISTS "User" CASCADE;
DROP TABLE IF EXISTS "Subject" CASCADE;
DROP TABLE IF EXISTS "user_subject_grades" CASCADE;

CREATE TABLE "Faculty"
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE "Group"
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(32) UNIQUE NOT NULL,
    faculty INTEGER REFERENCES "Faculty" (id)
);

-- Создание таблиц
CREATE TABLE "User"
(
    id             SERIAL PRIMARY KEY,
    username       VARCHAR(64) UNIQUE NOT NULL,
    password       VARCHAR(255)       NOT NULL,
    "roleType"         VARCHAR(10)        NOT NULL DEFAULT 'student',
    "studyGroup"        INTEGER REFERENCES "Group" (id),
    form_education VARCHAR(255)       NOT NULL DEFAULT 'Не указано',
    first_name     VARCHAR(64)        NOT NULL DEFAULT 'Не указано',
    last_name      VARCHAR(64)        NOT NULL DEFAULT 'Не указано',
    middle_name    VARCHAR(64)                 DEFAULT 'Не указано'
);

CREATE TABLE "Subject"
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE "Task"
(
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(128) UNIQUE NOT NULL,
    description       VARCHAR(2048),
    "maxSymbolsCount" INTEGER,
    "maxStringsCount" INTEGER,
    construction      VARCHAR(128),
    teacher_formula   VARCHAR,
    input_variables   VARCHAR,
    "Subject_id"      INTEGER             NOT NULL REFERENCES "Subject" (id)
);

CREATE TABLE "Solution"
(
    id                  SERIAL PRIMARY KEY,
    code                TEXT    NOT NULL,
    mark                INTEGER,
    "lengthTestResult"  BOOLEAN,
    "formulaTestResult" BOOLEAN,
    "autoTestResult"    INTEGER,
    status              VARCHAR,
    "User_id"           INTEGER NOT NULL REFERENCES "User" (id),
    "Task_id"           INTEGER REFERENCES "Task" (id)
);

CREATE TABLE "TestCase"
(
    id        SERIAL PRIMARY KEY,
    inp       VARCHAR(512) NOT NULL,
    out       VARCHAR(512) NOT NULL,
    "Task_id" INTEGER REFERENCES "Task" (id)
);

CREATE TABLE "TestResult"
(
    id            SERIAL PRIMARY KEY,
    passed        BOOLEAN NOT NULL,
    "TestCase_id" INTEGER NOT NULL REFERENCES "TestCase" (id),
    "Solution_id" INTEGER NOT NULL REFERENCES "Solution" (id)
);

CREATE TABLE "UserHasSubject"
(
    user_id    INTEGER NOT NULL REFERENCES "User" (id),
    subject_id INTEGER NOT NULL REFERENCES "Subject" (id),
    PRIMARY KEY (user_id, subject_id)
);

CREATE TABLE "user_subject_grades"
(
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES "User" (id),
    subject_id INTEGER NOT NULL REFERENCES "Subject" (id),
    grade      FLOAT
);

INSERT INTO "Faculty" (name)
VALUES ('Информационные системы и технологии'),
       ('Вычислительная техника и программное обеспечение');

INSERT INTO "Group" (name, faculty)
VALUES ('211-365', 1),
       ('211-366', 1),
       ('211-367', 2),
       ('211-368', 2);

-- Добавление пользователей
INSERT INTO "User" (username, password, "roleType", "studyGroup", form_education, first_name, last_name,
                    middle_name)
VALUES ('teacher', 'teacher', 'teacher', NULL, '', 'Иван',
        'Калмыков', 'Денисович'),
       ('student', 'student', 'student', 1, 'Платная',
        'Петров', 'Антон', 'Данилович');

-- Добавление дисциплин
INSERT INTO "Subject" (name)
VALUES ('Python'),
       ('С++'),
       ('Java'),
       ('C#');

-- Привязка пользователя к дисциплине
INSERT INTO "UserHasSubject" (user_id, subject_id)
VALUES (1, 1),
       (1, 2),
       (2, 1),
       (2, 4);

-- Добавление заданий
INSERT INTO "Task" (name, "Subject_id", description, "maxSymbolsCount", "maxStringsCount", teacher_formula,
                    input_variables)
VALUES ('Задание 1. Python - числовые типы', 1,
        'Задача на числовые типы\nПример входных данных: 1 2 3\nПример выходных данных: 0 2', 128, 10,
        'b1=a1+a2-a3\nb2=b1+a2', 'a1\na2\na3'),
       ('Задание 1. С++ - числовые типы', 2, 'Задача на числовые типы', 128, 10, 'c - d', 'a3, a4'),
       ('Задание 2. Python - строки', 1, 'Задача на строки', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 2. С++ - строки', 2, 'Задача на строки', 128, 10, 'c - d', 'a3, a4'),
       ('Задание 3. Python - списки', 1, 'Задача на списки', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 3. С++ - списки', 2, 'Задача на списки', 128, 10, 'c - d', 'a3, a4'),
       ('Задание 1. Java - числовые типы', 3, 'Задача на числовые типы', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 2. Java - строки', 3, 'Задача на строки', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 3. Java - списки', 3, 'Задача на списки', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 4. Java - массивы', 3, 'Задача на массивы', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 5. Java - классы', 3, 'Задача на классы', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 1. C# - числовые типы', 4, 'Задача на числовые типы', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 2. C# - строки', 4, 'Задача на строки', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 3. C# - списки', 4, 'Задача на списки', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 4. C# - массивы', 4, 'Задача на массивы', 128, 10, 'a + b', 'a1, a2'),
       ('Задание 5. C# - классы', 4, 'Задача на классы', 128, 10, 'a + b', 'a1, a2');

-- Добавление тестовых случаев
INSERT INTO "TestCase" (inp, out, "Task_id")
VALUES ('1 2 3', '0 2', 1),
       ('4 5 6', '3 8', 1),
       ('7 8 9', '6 14', 1),
       ('10 11 12', '9 20', 1),
       ('13 14 15', '12 26', 1),
       ('16 17 18', '15 32', 1),
       ('19 20 21', '18 38', 1),
       ('22 23 24', '21 44', 1),
       ('25 26 27', '24 50', 1),
       ('28 29 30', '27 56', 1),
       ('31 32 33', '30 62', 1),
       ('34 35 36', '33 68', 1),
       ('37 38 39', '36 74', 1),
       ('40 41 42', '39 80', 1),
       ('43 44 45', '42 86', 1),
       ('46 47 48', '45 92', 1),
       ('49 50 51', '48 98', 1),
       ('52 53 54', '51 104', 1),
       ('55 56 57', '54 110', 1),
       ('58 59 60', '57 116', 1);

-- Добавление решений
INSERT INTO "Solution" (code, "User_id", "Task_id")
VALUES ('print(''Hello, World!'')', 1, 1),
       ('print(''Hello, World!'')', 1, 3);

-- Добавление результатов тестирования
INSERT INTO "TestResult" (passed, "TestCase_id", "Solution_id")
VALUES (TRUE, 1, 1),
       (TRUE, 2, 2);

-- Выставление оценки
UPDATE "Solution"
SET mark = 100
WHERE id = 2;
