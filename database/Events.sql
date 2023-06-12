-- -----------------------------------------------------
-- Event delete_expired_reservations
-- -----------------------------------------------------

DROP EVENT IF EXISTS delete_expired_reservations;
CREATE EVENT delete_expired_reservations
ON SCHEDULE EVERY 1 DAY
DO
    DELETE FROM Reserve WHERE (DATE_ADD(date, INTERVAL 7 DAY) < DATE(NOW())) AND (approved = 1);
    

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
	CALL Check_books_available()