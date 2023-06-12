-- -----------------------------------------------------
-- Administrator
-- -----------------------------------------------------

-- 4.1.1. --------------------------------------------------------------------------------------------------
SET @year = 2021;
SET @month = 10;    

SELECT s.name school, COUNT(br.Books_ISBN) number_loans
FROM Schools s
INNER JOIN Books b ON b.Schools_id_school = s.id_school
INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN
WHERE
    CASE
        WHEN (@year != '' AND @month != '')
            THEN (YEAR(br.start_date) = @year AND MONTH(br.start_date) = @month)
        WHEN (@year = '' AND @month != '')
            THEN (MONTH(br.start_date) = @month)
        WHEN (@year != '' AND @month = '')
            THEN (YEAR(br.start_date) = @year)
    END
GROUP BY s.name;

-- 4.1.2. --------------------------------------------------------------------------------------------------
SET @category = "Science Fiction";

SELECT CONCAT(a.first_name, ' ', a.last_name) authors_names
FROM Authors a
INNER JOIN Authors_Books ab ON ab.Authors_id_author = a.id_author
INNER JOIN Books b ON b.ISBN = ab.Books_ISBN
INNER JOIN Categories_Books ca ON ca.Books_ISBN = b.ISBN
WHERE ca.Categories_category_name = @category
GROUP BY a.id_author;

SELECT CONCAT(u.first_name, ' ', u.last_name) teachers_names
FROM Users u
INNER JOIN Borrow bor ON bor.Users_id_user = u.id_user
INNER JOIN Books boo ON boo.ISBN = bor.Books_ISBN
INNER JOIN Categories_Books cb ON cb.Books_ISBN = boo.ISBN
WHERE (u.Roles_role = 'teacher' 
	AND cb.Categories_category_name = @category 
	AND bor.start_date > DATE_ADD(DATE(NOW()), INTERVAL -1 YEAR));

-- 4.1.3. --------------------------------------------------------------------------------------------------

SELECT CONCAT(u.first_name, " ", u.last_name) "Teachers names", COUNT(*) "Number of books borrowed"
FROM Users u
INNER JOIN Borrow b ON u.id_user = b.Users_id_user
WHERE (u.birth_date > DATE_ADD(DATE(NOW()), INTERVAL -40 YEAR)) AND (u.Roles_role = "teacher")
GROUP BY u.id_user
ORDER BY "Number of books borrowed" DESC
LIMIT 1;

-- 4.1.4. --------------------------------------------------------------------------------------------------

SELECT CONCAT(a.first_name, " ", a.last_name) "Authors names"
FROM Authors a
WHERE a.id_author NOT IN (SELECT distinct(a.id_author)
	FROM Authors a
	INNER JOIN Authors_Books ab ON a.id_author = ab.Authors_id_author
	INNER JOIN Books b ON ab.Books_ISBN = b.ISBN
	INNER JOIN Borrow br ON b.ISBN = br.Books_ISBN);
    
-- 4.1.5. --------------------------------------------------------------------------------------------------
    
SET @year = "2022";

SELECT o.id_operators, o.first_name, o.last_name, COUNT(br.Books_ISBN) AS Books_loaned 
FROM Operators o
INNER JOIN Schools s ON s.Operators_id_operators = o.id_operators  
INNER JOIN Books b ON b.Schools_id_school = s.id_school
INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN  
WHERE YEAR(br.start_date) = @year
GROUP BY o.id_operators, o.first_name, o.last_name
HAVING COUNT(br.Books_ISBN) > 20;

-- 4.1.6. --------------------------------------------------------------------------------------------------

SELECT T.Categories, COUNT(T.Categories) Borrowing_times
FROM (
	SELECT br.Books_ISBN ISBN, GROUP_CONCAT(cb.Categories_category_name) Categories, br.start_date
	FROM Borrow br
	INNER JOIN Books b ON b.ISBN = br.Books_ISBN
	INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN 
	WHERE br.Books_ISBN IN (SELECT Books_ISBN FROM categories_books GROUP BY Books_ISBN HAVING COUNT(Books_ISBN)=2)
	GROUP BY br.Books_ISBN, br.start_date) T
GROUP BY T.Categories
ORDER BY Borrowing_times DESC
LIMIT 3;

-- 4.1.7. --------------------------------------------------------------------------------------------------

SELECT CONCAT(a.first_name, " ", a.last_name) "Authors names", T.Nbr_books "Number of books" FROM Authors a
INNER JOIN (SELECT ab.Authors_id_author, COUNT(ab.Authors_id_author) AS Nbr_books
	FROM Authors_Books ab
	GROUP BY ab.Authors_id_author) T 
		ON T.Authors_id_author = a.id_author 
WHERE T.Nbr_books <= (SELECT MAX(T.Nbr_books) - 5 FROM 
	(SELECT ab.Authors_id_author, COUNT(ab.Authors_id_author) AS Nbr_books
	FROM Authors_Books ab
	GROUP BY ab.Authors_id_author) T);
    
    
-- -----------------------------------------------------
-- Operator
-- -----------------------------------------------------

-- 4.2.1. --------------------------------------------------------------------------------------------------

SET @id_op = 1;
SET @title = "";
SET @category = "Science fiction";
SET @author = "";
SET @copies = "";

SELECT b.*, cb.Categories_category_name FROM Books b
INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN
INNER JOIN Authors a ON a.id_author = ab.Authors_id_author
INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN
INNER JOIN Schools s ON s.id_school = b.Schools_id_school
WHERE s.Operators_id_operators = @id_op AND
	CASE 
		#title, category, author, copies
		WHEN (@title != "" AND @category != "" AND @author != "" AND @copies != "") 
			THEN (b.title = @title AND cb.Categories_category_name = @category AND a.last_name = @author AND b.available_copies = @copies)
        #title, category, author    
		WHEN (@title != "" AND @category != "" AND @author != "" AND @copies = "") 
			THEN (b.title = @title AND cb.Categories_category_name = @category AND a.last_name = @author)
        #title, category, copies    
		WHEN (@title != "" AND @category != "" AND @author = "" AND @copies != "") 
			THEN (b.title = @title AND cb.Categories_category_name = @category AND b.available_copies = @copies)
        #title, author, copies    
		WHEN (@title != "" AND @category = "" AND @author != "" AND @copies != "") 
			THEN (b.title = @title AND a.last_name = @author AND b.available_copies = @copies)
		#category, author, copies    
		WHEN (@title = "" AND @category != "" AND @author != "" AND @copies != "") 
			THEN (cb.Categories_category_name = @category AND a.last_name = @author AND b.available_copies = @copies)
		#category, author    
		WHEN (@title = "" AND @category != "" AND @author != "" AND @copies = "") 
			THEN (cb.Categories_category_name = @category AND a.last_name = @author)
		#category, copies    
		WHEN (@title = "" AND @category != "" AND @author = "" AND @copies != "") 
			THEN (cb.Categories_category_name = @category AND b.available_copies = @copies)
		#title, category   
		WHEN (@title != "" AND @category != "" AND @author = "" AND @copies = "") 
			THEN (b.title = @title AND cb.Categories_category_name = @category)
		#title, author   
		WHEN (@title != "" AND @category = "" AND @author != "" AND @copies = "") 
			THEN (b.title = @title AND a.last_name = @author)
		#title, copies
		WHEN (@title != "" AND @category = "" AND @author = "" AND @copies != "") 
			THEN (b.title = @title AND b.available_copies = @copies)
		#author, copies
		WHEN (@title = "" AND @category = "" AND @author != "" AND @copies != "") 
			THEN (a.last_name = @author AND b.available_copies = @copies)
		#title
		WHEN (@title != "" AND @category = "" AND @author = "" AND @copies = "") 
			THEN (b.title = @title)
		#category
		WHEN (@title = "" AND @category != "" AND @author = "" AND @copies = "") 
			THEN (cb.Categories_category_name = @category)
        #author
		WHEN (@title = "" AND @category = "" AND @author != "" AND @copies = "") 
			THEN (a.last_name = @author)
		#copies
		WHEN (@title = "" AND @category = "" AND @author = "" AND @copies != "") 
			THEN (b.available_copies = @copies)
	END;


-- 4.2.2. --------------------------------------------------------------------------------------------------
SET @id_op = 1;

SELECT u.first_name, u.last_name, DATEDIFF(DATE(NOW()), DATE_ADD(br.start_date, INTERVAL 7 DAY)) AS Delayed_days
FROM Users u 
INNER JOIN Borrow br ON br.Users_id_user = u.id_user
INNER JOIN Schools s ON s.id_school = u.Schools_id_school
WHERE (br.end_date IS NULL) 
	AND (DATE_ADD(br.start_date, INTERVAL 7 DAY) < DATE(NOW())) 
    AND br.approved = 1
    AND s.Operators_id_operators = @id_op;

-- 4.2.3. --------------------------------------------------------------------------------------------------
SET @id_op = 3;
SET @category = 'Science Fiction';
SET @id_user = '';

SELECT AVG(r.grade) AS avg_grade
FROM Review r
INNER JOIN Books b ON b.ISBN = r.Books_ISBN
INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN
INNER JOIN Schools s ON s.id_school = b.Schools_id_school
WHERE s.Operators_id_operators = @id_op AND 
	CASE
        WHEN (@id_user != '' AND @category != '')
            THEN (r.Users_id_user = @id_user AND cb.Categories_category_name = @category)
        WHEN (@id_user != '' AND @category = '')
            THEN (r.Users_id_user = @id_user)
        WHEN (@id_user = '' AND @category != '')
            THEN (cb.Categories_category_name = @category)
    END;

-- -----------------------------------------------------
-- User
-- -----------------------------------------------------

-- 4.3.1. --------------------------------------------------------------------------------------------------
SET @id_user = 1;
SET @title = "";
SET @category = "Crime/Noir";
SET @author = "";

SELECT b.*, a.first_name, a.last_name, cb.Categories_category_name 
FROM Books b
INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN
INNER JOIN Authors a ON a.id_author = ab.Authors_id_author
INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN
INNER JOIN Schools s ON s.id_school = b.Schools_id_school
WHERE s.id_school = (SELECT Schools_id_school FROM Users WHERE id_user = @id_user) AND
	CASE
		#title, category, author
		WHEN (@title != "" AND @category != "" AND @author != "") 
			THEN (b.title = @title AND cb.Categories_category_name = @category AND a.last_name = @author)
		#title, category
		WHEN (@title != "" AND @category != "" AND @author = "") 
			THEN (b.title = @title AND cb.Categories_category_name = @category)
		#category, author
		WHEN (@title = "" AND @category != "" AND @author != "") 
			THEN (cb.Categories_category_name = @category AND a.last_name = @author)
		#title, author
		WHEN (@title != "" AND @category = "" AND @author != "") 
			THEN (b.title = @title AND a.last_name = @author)
		#title
		WHEN (@title != "" AND @category = "" AND @author = "") 
			THEN (b.title = @title)
		#category
		WHEN (@title = "" AND @category != "" AND @author = "") 
			THEN (cb.Categories_category_name = @category)
		#author
		WHEN (@title = "" AND @category = "" AND @author != "") 
			THEN (a.last_name = @author)
	END;

-- For the ability to select a book and create a reservation request see procedure "Borrow_Or_Reserve"

-- 4.3.2. --------------------------------------------------------------------------------------------------

SET @id_user = "1";

SELECT b.ISBN, b.title, a.first_name, a.last_name, cb.Categories_category_name, br.start_date, br.end_date
FROM Books b
INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN
INNER JOIN Authors a ON a.id_author = ab.Authors_id_author
INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN
INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN
WHERE br.Users_id_user = @id_user AND br.approved = 1
ORDER BY br.start_date DESC;