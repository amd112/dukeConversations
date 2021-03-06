--Duke Conversations Database
--Insert statemtns to check restrictions on the tables 

--Ensuring the student ID giving a review applied to that dinner and attended
INSERT INTO Reviews VALUES 
  (5, 11, 'Great Dinner', 4, 9); 

--updating a key in applications 
UPDATE Applications SET date_time = NULL WHERE Student_id = '2016-09-06 07:30:00';

--make a dinner for a professor that doesn't exist 
INSERT INTO Dinners VALUES 
  (6, '2015-10-12 6:00:00', 106);

--cerate a review for a dinner that does not exist 
INSERT INTO Reviews VALUES 
  (15, 3, 'fun time', 7, 8);

--create a review by a student who does not exist in the database
INSERT INTO Reviews VALUES
  (5, 11, 'awesome', 5, 7);

--assign a student a major that does not exist
INSERT INTO Students VALUES 
  (11, 'Alan Khaykin', NULL, 'ak374', 1487283948, 2019,'HarryPotter', 'Male');

--create a student with an invalid netID 
INSERT INTO Students VALUES 
  (12, 'Alan Khaykin', NULL, NULL, 1487283948, 2019, 'Public Policy', 'Male');
  (12, 'Alan Khaykin', NULL, 'sasas1118', 1487283948, 2019,'Public Policy', 'Male');

--create a student with a phone number that is not valid  
INSERT INTO Students VALUES
  (13, 'Alan Khaykin', NULL, 'ak374', NULL, 2019, 'Public Policy', 'Male');
