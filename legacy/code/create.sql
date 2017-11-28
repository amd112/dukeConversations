CREATE TABLE Students
(unique_id INTEGER NOT NULL PRIMARY KEY, 
 name VARCHAR(30) NOT NULL,
 food_restrictions VARCHAR(30),
 netid VARCHAR(8) NOT NULL,
 phone_number BIGINT NOT NULL,
 year INTEGER NOT NULL,
 major VARCHAR(50),
 pronouns VARCHAR(20)
);

CREATE TABLE Professors
(unique_id INTEGER NOT NULL PRIMARY KEY,
 name VARCHAR(30) NOT NULL,
 food_restrictions VARCHAR(30),
 netid VARCHAR(8) NOT NULL,
 gender VARCHAR(1)
);

CREATE TABLE Dinners
(dinner_id SERIAL UNIQUE PRIMARY KEY,
 date_time TIMESTAMP NOT NULL,
 professor_id INTEGER NOT NULL REFERENCES Professors(unique_id)
);

CREATE TABLE Applications
(student_id INTEGER NOT NULL REFERENCES Students(unique_id),
 dinner_id INTEGER NOT NULL REFERENCES Dinners(dinner_id),
 selected BOOLEAN NULL,
 attended BOOLEAN NULL,
 date_time TIMESTAMP NOT NULL,
 interest VARCHAR(400) NOT NULL
 PRIMARY KEY(student_id, dinner_id)
);

--Need to keep Reviews table as flexible as possible as they do A/B testing
CREATE TABLE Reviews
(dinner_id INTEGER NOT NULL REFERENCES Dinners(dinner_id),
 student_id INTEGER NOT NULL REFERENCES Students(unique_id),
 conversation_comments VARCHAR(1000),
 food_comments VARCHAR(1000),
 food_grade SMALLINT,
 conversation_grade SMALLINT,
 PRIMARY KEY(dinner_id, student_id)
);

CREATE VIEW Students_Data AS
SELECT unique_id, netid, name, food_restrictions, phone_number, year, major, pronouns,
	  (SELECT COUNT(*) FROM Applications WHERE s.unique_id = student_id) AS applied, 
	  (SELECT COUNT(*) FROM Applications WHERE s.unique_id = student_id AND selected = 't') AS accepted
FROM Students AS s;

CREATE VIEW Professors_Data AS
SELECT name, food_restrictions, gender,
	  (SELECT COUNT(*) FROM Reviews WHERE dinner_id IN 
		 (SELECT dinner_id FROM Dinners WHERE professor_id = p.unique_id)) AS num_reviews,
	  (SELECT AVG(conversation_grade) FROM Reviews WHERE dinner_id IN 
		 (SELECT dinner_id FROM Dinners WHERE professor_id = p.unique_id)) AS avg_reviews,
	  (SELECT COUNT(*) FROM Dinners WHERE professor_id = p.unique_id) AS num_dinners
FROM Professors as p;

-- BEGINING
-- OF
-- TRIGGERS
-- (d) Make sure that being late gets at least -10 

CREATE FUNCTION Went_To_Dinner() RETURNS TRIGGER AS $$
BEGIN 
  IF (NEW.dinner_id, NEW.student_id) NOT IN 
			(SELECT dinner_id, student_id
			 FROM Applications 
			 WHERE student_id = NEW.student_id 
				AND selected = 1
				AND attended = 1) THEN
    RAISE EXCEPTION 'No reviews for dinners that were not attended.';
	RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql; 
 
CREATE TRIGGER Went_To_Dinner
  BEFORE INSERT OR UPDATE ON Reviews
  FOR EACH ROW
  EXECUTE PROCEDURE Went_To_Dinner();
  

  
  
CREATE FUNCTION Valid_netid() RETURNS TRIGGER AS $$
BEGIN 
  IF NEW.netid NOT ~* '[abcdefghijklmnopqrstuvwxyz]+[0123456789]*'  THEN
    RAISE EXCEPTION 'Not a valid netid.';
	RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql; 
 
CREATE TRIGGER Valid_netid
  BEFORE INSERT OR UPDATE ON Students
  FOR EACH ROW
  EXECUTE PROCEDURE Valid_netid();

-- END
-- OF 
-- TRIGGERS

--Sample Data
INSERT INTO Students VALUES
	(1, 'Aashna Aggarwal', 'Vegetarian', 'aa373', 9174974486, 2019, NULL, 'she/her/hers'),
	(2, 'Adaiya Granberry', NULL, 'ag370', 2539056580, 2019, 'Public Policy', NULL),
	(3, 'Anne Driscoll', 'Vegetarian', 'amd112', 9176553632, 2018, 'Statistics', 'she/her/hers'),
	(4, 'Arthur Wu', NULL, 'aw258', 9848887018, 2019, 'Statistics', 'he/him/his'),
	(5, 'Candice Dunn', 'No Cheese', 'cld36', 8569041855, 2017, NULL, NULL),
	(6, 'Lauren Hagedorn', 'Gluten Intolerant', 'lph10', 3106477767, 2017, 'Psychology, Environmental Science', 'she/her/hers'),
	(7, 'Mitchell Abrams', 'Kosher', 'mza2', 8455966009, 2019, NULL, 'he/him/his'),
	(8, 'Misty Sha', NULL, 'ys114', 9198088119, 2017, NULL, NULL),
	(9, 'Nikolaus Mayr', NULL, 'nm183', 9843779630, 2017, NULL, 'he/him/his'),
	(10, 'Sean Gilbert', 'Vegetarian', 'smg41', 2402718022, 2018, 'Political Science', 'he/him/his');

INSERT INTO Professors VALUES
	(101, 'Steve Nowicki', NULL, 'sn123', 'm'),
	(102, 'Dan Ariely', 'Vegetarian', 'da45', 'm'),
	(103, 'David Banks', NULL, 'dbanks', 'm'),
	(104, 'Clark Bray', NULL, 'bray2', 'm'),
	(105, 'Richard Broadhead', NULL, 'rhb1', 'm');

INSERT INTO Dinners VALUES
	('2016-09-06 07:30:00', 101),
	('2015-09-08 06:00:00', 102),
	('2016-09-20 06:45:00', 103),
	('2016-10-04 08:00:00', 104),
	('2015-10-13 05:30:00', 105);

INSERT INTO Applications (student_id, dinner_id, date_time, interest) VALUES
	(1, 1, '2016-08-06 07:30:00', 'Best prof ever'),
	(2, 1, '2016-09-01 04:30:00', 'Took a class with him sounds lit'),
	(3, 2, '2015-08-15 01:30:00', 'tbh I want free food'),
	(4, 2, '2015-09-06 07:35:33', 'really interested in the topic'),
	(5, 2, '2015-09-07 04:00:00', 'want to meet new people'),
	(6, 3, '2016-09-06 07:30:00', 'food on campus sucks'),
	(7, 4, '2016-9-28 07:21:17', 'do i need a reason'),
	(8, 4, '2016-10-01 08:30:00', 'sounds lit'),
	(9, 5, '2015-09-14 05:35:53', 'always wanted to meet him!'),
	(10, 5, '2015-10-06 03:33:33', 'not sure really');

INSERT INTO Reviews VALUES
	(2, 3, 'Great conversation!', 'nom', 8, 10),
	(3, 6, 'The chicken was delicious', 'boo', 10, 7),
	(4, 8, 'Clark Bray is the best', 'so good', 8, 10);