CREATE TABLE User
(
    userid   INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(40)  NOT NULL
);
CREATE TABLE Line
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    blogname VARCHAR(100) NOT NULL,
    text     VARCHAR(40)  NOT NULL
);
CREATE TABLE Blog
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    blogname VARCHAR(100) NOT NULL
);


INSERT INTO User (username, password)
VALUES ('taft_scp', 'vrnctf{sq1_un1on_uni3n_un20n}');