-- -----------------------------------------------------
-- Event delete_expired_reservations
-- -----------------------------------------------------

DROP EVENT IF EXISTS delete_expired_reservations;
CREATE EVENT delete_expired_reservations
ON SCHEDULE EVERY 1 DAY
DO
    DELETE FROM Reserve WHERE (DATE_ADD(date, INTERVAL 7 DAY) < DATE(NOW())) AND (approved = 1);
    
    
-- -----------------------------------------------------
-- Trigger books_return
-- -----------------------------------------------------
    
DROP TABLE IF EXISTS Return_books;
CREATE TABLE Return_books (
  id_user INT NOT NULL,
  ISBN VARCHAR(45) NOT NULL,
  end DATE NULL
);

DROP TRIGGER IF EXISTS books_return;
DELIMITER //

CREATE TRIGGER books_return
AFTER INSERT ON Return_books
FOR EACH ROW
BEGIN
    UPDATE Borrow SET end_date = DATE(NOW()) 
    WHERE end_date IS NULL AND approved = 1 AND Books_ISBN = NEW.ISBN AND Users_id_user = NEW.id_user AND DATE(NOW()) = NEW.end;
    
    INSERT INTO Borrow (Books_ISBN,Users_id_user,start_date,end_date,approved) 
    SELECT r.Books_ISBN, r.Users_id_user, DATE(NOW()), NULL, 1
    FROM Reserve r
    WHERE (r.Books_ISBN = NEW.ISBN) AND r.approved = 1 AND (EXISTS (SELECT * FROM Reserve rr INNER JOIN Return_books rb ON rr.Books_ISBN = rb.ISBN WHERE rr.Books_ISBN = rb.ISBN));

	DELETE FROM Reserve WHERE (Books_ISBN = NEW.ISBN) AND approved = 1;
END //

DELIMITER ;

-- -----------------------------------------------------
-- Event Erase_Return_books
-- -----------------------------------------------------

DROP EVENT IF EXISTS Erase_Return_books;
CREATE EVENT Erase_Return_books
ON SCHEDULE EVERY 1 HOUR
DO
    DELETE FROM Return_books;
    
-- -----------------------------------------------------
-- Event Check_availability
-- -----------------------------------------------------    
    
DROP EVENT IF EXISTS Check_availability;
CREATE EVENT Check_availability
ON SCHEDULE EVERY 10 SECOND
DO
	CALL Check_books_available();
