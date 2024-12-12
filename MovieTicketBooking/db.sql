CREATE TABLE shows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL
);

CREATE TABLE seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    show_id INT NOT NULL,
    row_num INT NOT NULL,
    col_num INT NOT NULL,
    status TINYINT NOT NULL DEFAULT 0,
    FOREIGN KEY (show_id) REFERENCES shows(id)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    show_id INT NOT NULL,
    user_name VARCHAR(100),
    seat_row INT,
    seat_col INT,
    FOREIGN KEY (show_id) REFERENCES shows(id)
);


INSERT INTO shows (movie_name, date_time) VALUES
('Interstellar','2024-12-10 18:00:00'),
('The Dark Knight', '2024-12-10 21:00:00'),
('Inception', '2024-12-11 18:00:00'),
('Avengers: Endgame','2024-12-11 21:00:00'),
('Dune', '2024-12-11 21:00:00'),
('The Matrix', '2024-12-12 21:00:00');

select * from seats  ;

insert into seats (show_id, row_num, col_num, status)
select 1 as show_id, r as row_num, c as col_num, 0 as status
FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
     (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
order by row_num, col_num;

insert into seats (show_id, row_num, col_num, status)
select 2 as show_id, r as row_num, c as col_num, 0 as status
FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
     (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
order by row_num, col_num;

insert into seats (show_id, row_num, col_num, status)
select 3 as show_id, r as row_num, c as col_num, 0 as status
FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
     (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
order by row_num, col_num;

insert into seats (show_id, row_num, col_num, status)
select 4 as show_id, r as row_num, c as col_num, 0 as status
FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
     (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
order by row_num, col_num;

insert into seats (show_id, row_num, col_num, status)
select 5 as show_id, r as row_num, c as col_num, 0 as status
FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
     (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
order by row_num, col_num;

insert into seats (show_id, row_num, col_num, status)
select 6 as show_id, r as row_num, c as col_num, 0 as status
FROM (SELECT 1 AS r UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) row_numbers,
     (SELECT 1 AS c UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) col_numbers
order by row_num, col_num;


select * from seats where show_id = 5;
SELECT * FROM seats WHERE show_id = 6 LIMIT 100;
SELECT show_id, COUNT(*) AS total_seats FROM seats GROUP BY show_id;




drop table shows


