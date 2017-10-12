CREATE TABLE Students
(unique_id INTEGER NOT NULL PRIMARY KEY, 
 name VARCHAR(30) NOT NULL,
 food_restrictions VARCHAR(30),
 netid VARCHAR(8) NOT NULL,
 phone_number BIGINT NOT NULL,
 year INTEGER NOT NULL,
 major VARCHAR(50),
 gender VARCHAR(10)
);

CREATE TABLE Professors
(unique_id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(30) NOT NULL,
 food_restrictions VARCHAR(30),
 netid VARCHAR(8) NOT NULL
);

CREATE TABLE Dinners
(dinner_id INTEGER NOT NULL PRIMARY KEY,
 date_time TIMESTAMP NOT NULL,
 professor_id INTEGER NOT NULL REFERENCES Professors(unique_id)
);

CREATE TABLE Applications
(student_id INTEGER NOT NULL REFERENCES Students(unique_id),
 dinner_id INTEGER NOT NULL REFERENCES Dinners(dinner_id),
 drive_num INTEGER,
 selected BOOLEAN NULL,
 date_time TIMESTAMP NOT NULL,
 PRIMARY KEY(student_id, dinner_id)
);

CREATE TABLE Reviews
(dinner_id INTEGER NOT NULL REFERENCES Dinners(dinner_id),
 student_id INTEGER NOT NULL REFERENCES Students(unique_id),
 comments VARCHAR(1000),
 food_grade SMALLINT,
 conversation_grade SMALLINT,
 PRIMARY KEY(dinner_id, student_id)
);

--Sample Data
INSERT INTO Students VALUES
	(1, 'Aashna Aggarwal', 'Vegetarian', 'aa373', 9174974486, 2019, NULL, 'Female'),
	(2, 'Adaiya Granberry', NULL, 'ag370', 2539056580, 2019, 'Public Policy', NULL),
	(3, 'Anne Driscoll', 'Vegetarian', 'amd112', 9176553632, 2018, 'Statistics', 'Female'),
	(4, 'Arthur Wu', NULL, 'aw258', 9848887018, 2019, 'Statistics', 'Male'),
	(5, 'Candice Dunn', 'No Cheese', 'cld36', 8569041855, 2017, NULL, NULL),
	(6, 'Lauren Hagedorn', 'Gluten Intolerant', 'lph10', 3106477767, 2017, 'Psychology, Environmental Science', 'Female'),
	(7, 'Mitchell Abrams', 'Kosher', 'mza2', 8455966009, 2019, NULL, 'Male'),
	(8, 'Misty Sha', NULL, 'ys114', 9198088119, 2017, NULL, NULL),
	(9, 'Nikolaus Mayr', NULL, 'nm183', 9843779630, 2017, NULL, 'Male'),
	(10, 'Sean Gilbert', 'Vegetarian', 'smg41', 2402718022, 2018, 'Political Science', 'Male');

INSERT INTO Professors VALUES
	(101, 'Steve Nowicki', NULL, 'sn123'),
	(102, 'Dan Ariely', 'Vegetarian', 'da45'),
	(103, 'David Banks', NULL, 'dbanks'),
	(104, 'Clark Bray', NULL, 'bray2'),
	(105, 'Richard Broadhead', NULL, 'rhb1');

INSERT INTO Dinners VALUES
	(1, '2016-09-06 07:30:00', 101),
	(2, '2015-09-08 06:00:00', 102),
	(3, '2016-09-20 06:45:00', 103),
	(4, '2016-10-04 08:00:00', 104),
	(5, '2015-10-13 05:30:00', 105);

INSERT INTO Applications VALUES
	(1, 1, NULL, TRUE, '2016-08-06 07:30:00'),
	(2, 1, 2, TRUE, '2016-09-01 04:30:00'),
	(3, 2, NULL, TRUE, '2015-08-15 01:30:00'),
	(4, 2, NULL, TRUE, '2015-09-06 07:35:33'),
	(5, 2, NULL, FALSE, '2015-09-07 04:00:00'),
	(6, 3, 3, TRUE, '2016-09-06 07:30:00'),
	(7, 4, NULL, FALSE, '2016-9-28 07:21:17'),
	(8, 4, 1, TRUE, '2016-10-01 08:30:00'),
	(9, 5, NULL, FALSE, '2015-09-14 05:35:53'),
	(10, 5, 1, TRUE, '2015-10-06 03:33:33');

INSERT INTO Reviews VALUES
	(2, 3, 'Great conversation!', 8, 10),
	(3, 6, 'The chicken was delicious', 10, 7),
	(4, 8, 'Clark Bray is the best', 8, 10);