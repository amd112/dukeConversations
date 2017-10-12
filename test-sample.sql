CREATE VIEW Students_Data 
SELECT netid, name, food_restrictions, phone_number, year, major, gender,
	  (SELECT COUNT(*) FROM Applications WHERE s.unique_id = student_id) AS applied, 
	  (SELECT COUNT(*) FROM Applications WHERE s.unique_id = student_id AND selected = 1) AS accepted,
	  
FROM Students AS s;

CREATE VIEW Professors_Data
SELECT name, food_restrictions, 
	  (SELECT COUNT(*) FROM Reviews WHERE dinner_id IN 
		 (SELECT dinner_id FROM Dinners WHERE professor_id = p.unique_id)) AS num_reviews,
	  (SELECT AVG(*) FROM Reviews WHERE dinner_id IN 
		 (SELECT dinner_id FROM Dinners WHERE professor_id = p.unique_id)) AS avg_reviews,
	  (SELECT COUNT(*) FROM Dinners WHERE professor_id = p.unique_id) AS num_dinners
FROM Professors as p;


SELECT * 
FROM Students_Data AS s, Applications AS a
WHERE s.unique_id = a.student_id AND a.dinner_id = 4;

SELECT * 
FROM Dinners AS d, Professors AS p
WHERE p.unique_id = d.professor_id AND p.name = 'Clark Bray';