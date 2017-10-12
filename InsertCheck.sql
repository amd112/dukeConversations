--Duke Conversations Database
--Insert statemtns to check restrictions on the tables 

--Ensuring the student ID giving a review applied to that dinner and attended
--CHANGE TO DINNER ID THAT EXISTS
INSERT INTO Reviews VALUES 
--CHANGE TO VALID UNIQUE ID
  (15, 0101010, 'Great Dinner', 4, 2); 

--updating a key in applications 
UPDATE Applications SET Student_id = 'aa374' WHERE Student_id = 'aa373';

--make prof_id in Professors reference a professor that doesn't exist 
--CHANGE TO VALID UNIQUE ID
INSERT INTO Professors VALUES 
  (0101010, 'Astrachan', 'peanut allergy', 'sas118', 5, 4, 3);

--cerate a review for a dinner that does not exist 
INSERT INTO Reviews VALUES 
  (15, 'laj24', 'fun time', 5, 3);

--create a review by a student who does not exist in the database
--CHANGE TO DINNER ID THAT EXISTS
INSERT INTO Reviews VALUES
  (15, 'sas118', 'awesome', 5, 7);

--assign a student a major that does not exist
--CHANGE TO VALID UNIQUE ID
INSERT INTO Students VALUES 
  (0101010, 'Alan Khaykin', 'none', 'ak374', 1, 1, 2019, 'HarryPotter', 'male');

--create a student with an invalid netID 
--CHANGE TO VALID UNIQUE ID
INSERT INTO Students VALUES 
  (0101010, 'Alan Khaykin', 'none', 'abcdef', 1, 1, 2019);

--create a student with a phone number that is not valid 
--phone number is not currently in the students table 
--INSERT INTO Students VALUES
--(0101010, 'Alan Khaykin', 'none', 'abcdef', 1, 1, 2019, 12345678999);