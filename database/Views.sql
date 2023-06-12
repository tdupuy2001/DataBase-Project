-- -----------------------------------------------------
-- View Registered_people
-- -----------------------------------------------------

DROP VIEW IF EXISTS Registered_people ;
CREATE VIEW Registered_people AS
	SELECT id_admin id, username, password, role FROM Administrator
	UNION
	SELECT id_operators id, username, password, role FROM Operators WHERE approved = "1"
    UNION
    SELECT id_user id, username, password, Roles_role role FROM Users WHERE approved = "1";
    
    
-- -----------------------------------------------------
-- View Registration_demand
-- -----------------------------------------------------

DROP VIEW IF EXISTS Registration_demand ;
CREATE VIEW Registration_demand AS
	SELECT * FROM Users WHERE approved = "0";
    
-- -----------------------------------------------------
-- View Review_demand
-- -----------------------------------------------------

DROP VIEW IF EXISTS Review_demand ;
CREATE VIEW Review_demand AS
	SELECT * FROM Review WHERE approved = "0";
    
-- -----------------------------------------------------
-- View Borrow_demand
-- -----------------------------------------------------

DROP VIEW IF EXISTS Borrow_demand ;
CREATE VIEW Borrow_demand AS
	SELECT * FROM Borrow WHERE approved = "0";
    
-- -----------------------------------------------------
-- View Books_borrowed
-- -----------------------------------------------------

DROP VIEW IF EXISTS Books_borrowed ;
CREATE VIEW Books_borrowed AS
	SELECT br.Users_id_user id_user, br.Books_ISBN ISBN, br.start_date start_date, s.id_school id_school, u.Roles_role role
    FROM Borrow br
    INNER JOIN Users u ON u.id_user = br.Users_id_user
    INNER JOIN Schools s ON s.id_school = u.Schools_id_school
    WHERE br.end_date IS NULL AND br.approved = 1;
 
-- -----------------------------------------------------
-- View Available_books
-- -----------------------------------------------------
 
DROP VIEW IF EXISTS Available_books;
CREATE VIEW Available_books AS
	SELECT b.ISBN, b.title, b.number_of_pages, b.language, b.summary, b.keywords, s.id_school FROM Books b
	INNER JOIN Schools s ON s.id_school = b.Schools_id_school
	WHERE (b.ISBN NOT IN (SELECT b.ISBN FROM Books b
		INNER JOIN (SELECT bb.ISBN, COUNT(*) compt FROM Books_borrowed bb GROUP BY bb.ISBN) T 
        ON T.ISBN = b.ISBN WHERE b.available_copies = T.compt)) 
	GROUP BY ISBN;

