-- -----------------------------------------------------
-- Procedure Borrow_Or_Reserve
-- -----------------------------------------------------

DROP PROCEDURE IF EXISTS Borrow_Or_Reserve;
DELIMITER //

CREATE PROCEDURE Borrow_Or_Reserve(IN book_ISBN VARCHAR(255), IN user INT, OUT location VARCHAR(45))
BEGIN
    DECLARE Count INT;

    SELECT COUNT(*) INTO Count
    FROM available_books
    WHERE ISBN = book_ISBN AND id_school = (SELECT Schools_id_school FROM Users WHERE id_user = user);

    IF Count > 0 THEN
        INSERT INTO Borrow (Books_ISBN,Users_id_user,start_date,end_date,approved) VALUES (book_ISBN, user, DATE(NOW()), NULL, 0);
        SET location = "Borrow";
    ELSE
		INSERT INTO Reserve (Books_ISBN,Users_id_user,date,approved) VALUES (book_ISBN, user, DATE(NOW()), 0);
		SET location = "Reserve";
    END IF;
END //

DELIMITER ;

-- -----------------------------------------------------
-- Procedure Check_books_available
-- -----------------------------------------------------

DROP PROCEDURE IF EXISTS Check_books_available;
DELIMITER // 

CREATE PROCEDURE Check_books_available()
	BEGIN
		INSERT INTO Borrow (Books_ISBN,Users_id_user,start_date,end_date,approved) 
		SELECT r.Books_ISBN, r.Users_id_user, DATE(NOW()), NULL, 1
		FROM Reserve r
		INNER JOIN available_books ab ON ab.ISBN = r.Books_ISBN
		WHERE (r.Books_ISBN = ab.ISBN) AND r.approved = 1 AND 
        (EXISTS (SELECT * FROM Reserve rr INNER JOIN available_books ab ON ab.ISBN = r.Books_ISBN WHERE rr.Books_ISBN = ab.ISBN));

		DELETE FROM Reserve WHERE (Books_ISBN = (SELECT bb.ISBN FROM books_borrowed bb)) 
        AND (Users_id_user = (SELECT bb.id_user FROM books_borrowed bb)) AND approved = 1;
	END//
    
DELIMITER ;