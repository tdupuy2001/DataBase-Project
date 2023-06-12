from flask import Flask, render_template, request, flash, redirect, url_for, abort,session 
from projectDB import app, db 
from projectDB.login.forms import LoginForm, ChangepasswordForm, ChangemailForm, SearchForm, ReviewForm, Search_op_Form, add_book_Form, return_book_Form, check_user_Form, rating_book_Form,school_loans_Form,operator_loans_Form,affiliation_category_Form,add_operator_Form,add_school_Form
import MySQLdb.cursors

@app.route("/login" , methods=["GET","POST"])

def login(): 
    form=LoginForm()
    if(request.method == "POST" and form.validate_on_submit()):
       personnal_information = form.__dict__
       username=personnal_information["username"].data
       password=personnal_information["password"].data
       username=username.strip()
       password=password.strip()
       try:
           query=f"SELECT * FROM registered_people  WHERE username='{username}' and password='{password}' "
           cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
           cur.execute(query)
           account=cur.fetchone()
           if account:
               session['loggedin'] = True
               session['username'] = account['username']
               session['id'] = account['id']
               session['role'] = account['role']
               if account['role']=='student':
                   return redirect(url_for("student"))
               elif account['role']=='teacher':
                   return redirect(url_for("teacher"))
               elif account['role']=='operator':
                   return redirect(url_for("operator"))
               else:
                   return redirect(url_for("administrator"))
           else:
               cur.close()
               msg = 'Incorrect username/password!'
               flash(msg)
       except Exception as e: 
           flash(str(e), "danger")     
    return render_template("login.html",form=form)

@app.route("/login/logout")

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('role',None)
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route("/student", methods=["GET","POST"])

def student():
    form=SearchForm()
    if 'loggedin' in session and session['role']=='student':
        if(request.method == "POST" and form.validate_on_submit()):
           book_information = form.__dict__
           book_title=book_information["title"].data
           book_category=book_information["category"].data
           book_author=book_information["author"].data
           book_title=book_title.strip()
           book_category=book_category.strip()
           book_author=book_author.strip()
           try:
               query = f"SELECT b.ISBN ISBN,b.title title, b.number_of_pages number_pages, b.language language, b.summary summary, b.keywords keywords FROM Books b INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN INNER JOIN Authors a ON a.id_author = ab.Authors_id_author INNER JOIN (SELECT Books_ISBN, GROUP_CONCAT(Categories_category_name) Categories_category_name FROM Categories_Books GROUP BY Books_ISBN) cb ON cb.Books_ISBN = b.ISBN INNER JOIN Schools s ON s.id_school = b.Schools_id_school WHERE s.id_school = (SELECT Schools_id_school FROM Users WHERE id_user = '{session['id']}') AND CASE WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' != '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' = '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' != '') THEN (UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' = '') THEN 1 END"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               return render_template('landing_user.html',link1='/student',link2='/student/profile',form=form,res=res)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query=f"SELECT b.ISBN ISBN,b.title title, b.number_of_pages number_pages, b.language language, b.summary summary, b.keywords keywords FROM Books b INNER JOIN Schools s ON s.id_school = b.Schools_id_school INNER JOIN Users u ON s.id_school = u.Schools_id_school WHERE (b.ISBN NOT IN (SELECT b.ISBN FROM Books b INNER JOIN (SELECT bb.ISBN, COUNT(*) compt FROM Books_borrowed bb GROUP BY bb.ISBN) T ON T.ISBN = b.ISBN WHERE b.available_copies = T.compt)) AND (u.Schools_id_school = (SELECT Schools_id_school FROM Users WHERE id_user = '{session['id']}')) GROUP BY ISBN"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            query=f"SELECT s.name school_name FROM Schools s INNER JOIN Users u ON s.id_school=u.Schools_id_school WHERE u.id_user='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            a=cur.fetchone()
            cur.close()
            title=f"Available books in {a['school_name']} school:"
            return render_template('landing_user.html',link1='/student',link2='/student/profile',form=form,title=title,res=res)
    return redirect(url_for('login'))


@app.route("/teacher", methods=["GET","POST"])

def teacher():
    form=SearchForm()
    if 'loggedin' in session and session['role']=='teacher':
        if(request.method == "POST" and form.validate_on_submit()):
           book_information = form.__dict__
           book_title=book_information["title"].data
           book_category=book_information["category"].data
           book_author=book_information["author"].data
           book_title=book_title.strip()
           book_category=book_category.strip()
           book_author=book_author.strip()
           try:
               query = f"SELECT b.ISBN ISBN,b.title title, b.number_of_pages number_pages, b.language language, b.summary summary, b.keywords keywords FROM Books b INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN INNER JOIN Authors a ON a.id_author = ab.Authors_id_author INNER JOIN (SELECT Books_ISBN, GROUP_CONCAT(Categories_category_name) Categories_category_name FROM Categories_Books GROUP BY Books_ISBN) cb ON cb.Books_ISBN = b.ISBN INNER JOIN Schools s ON s.id_school = b.Schools_id_school WHERE s.id_school = (SELECT Schools_id_school FROM Users WHERE id_user = '{session['id']}') AND CASE WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' != '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' = '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' != '') THEN (UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' = '') THEN 1 END"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               return render_template('landing_user.html',link1='/teacher',link2='/teacher/profile',form=form,res=res)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query=f"SELECT b.ISBN ISBN,b.title title, b.number_of_pages number_pages, b.language language, b.summary summary, b.keywords keywords FROM Books b INNER JOIN Schools s ON s.id_school = b.Schools_id_school INNER JOIN Users u ON s.id_school = u.Schools_id_school WHERE (b.ISBN NOT IN (SELECT b.ISBN FROM Books b INNER JOIN (SELECT bb.ISBN, COUNT(*) compt FROM Books_borrowed bb GROUP BY bb.ISBN) T ON T.ISBN = b.ISBN WHERE b.available_copies = T.compt)) AND (u.Schools_id_school = (SELECT Schools_id_school FROM Users WHERE id_user = '{session['id']}')) GROUP BY ISBN"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            query=f"SELECT s.name school_name FROM Schools s INNER JOIN Users u ON s.id_school=u.Schools_id_school WHERE u.id_user='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            a=cur.fetchone()
            cur.close()
            title=f"Available books in {a['school_name']} school:"
            return render_template('landing_user.html',link1='/teacher',link2='/teacher/profile',form=form,title=title,res=res)
    return redirect(url_for('login'))


@app.route("/student/profile")
def profile_student():
    form=ReviewForm()
    if 'loggedin' in session and session['role']=='student': 
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        query=f"SELECT u.first_name first_name, u.last_name last_name, u.birth_date birth_date, u.email email, u.username username, u.password password, s.name school FROM Users u INNER JOIN Schools s ON s.id_school = u.Schools_id_school WHERE u.id_user = '{session['id']}'"           
        cur.execute(query)
        account = cur.fetchone()
        cur.close()
        query=f"SELECT b.ISBN ISBN, b.title title, CONCAT(a.first_name ,' ', a.last_name) author_name, cb.Categories_category_name category, br.start_date start_date, br.end_date end_date FROM Books b INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN INNER JOIN Authors a ON a.id_author = ab.Authors_id_author INNER JOIN (SELECT Books_ISBN, GROUP_CONCAT(Categories_category_name) Categories_category_name FROM Categories_Books GROUP BY Books_ISBN) cb ON cb.Books_ISBN = b.ISBN INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN WHERE br.Users_id_user = '{session['id']}' AND br.approved = 1 ORDER BY br.start_date DESC"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('profile_student.html', account=account,link1='/student', link2='/student/profile',res=res,form=form)
    return redirect(url_for('login'))


@app.route("/teacher/profile")
def profile_teacher():
    form=ReviewForm()
    if 'loggedin' in session and session['role']=='teacher': 
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        query=f"SELECT u.first_name first_name, u.last_name last_name, u.birth_date birth_date, u.email email, u.username username, u.password password, s.name school FROM Users u INNER JOIN Schools s ON s.id_school = u.Schools_id_school WHERE u.id_user = '{session['id']}'"           
        cur.execute(query)
        account = cur.fetchone()
        cur.close()
        query=f"SELECT b.ISBN ISBN, b.title title, CONCAT(a.first_name ,' ', a.last_name) author_name, cb.Categories_category_name category, br.start_date start_date, br.end_date end_date FROM Books b INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN INNER JOIN Authors a ON a.id_author = ab.Authors_id_author INNER JOIN (SELECT Books_ISBN, GROUP_CONCAT(Categories_category_name) Categories_category_name FROM Categories_Books GROUP BY Books_ISBN) cb ON cb.Books_ISBN = b.ISBN INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN WHERE br.Users_id_user = '{session['id']}' AND br.approved = 1 ORDER BY br.start_date DESC"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('profile_teacher.html', account=account,link1='/teacher', link2='/teacher/profile',res=res,form=form)
    return redirect(url_for('login'))

    

@app.route("/teacher/profile/changepassword",methods=["GET","POST"])

def changepassword_teacher():
    
    form=ChangepasswordForm()
    if 'loggedin' in session and session['role']=='teacher': 
        if(request.method == "POST" and form.validate_on_submit()):
            personnal_information = form.__dict__
            old_password=personnal_information["old_password"].data
            new_password=personnal_information["new_password"].data
            old_password=old_password.strip()
            new_password=new_password.strip()
            query=f"SELECT password FROM Users where id_user ='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            res=cur.fetchone()
            if res['password'].strip()!=old_password:
                cur.close()
                flash('Wrong old password',"danger")
            else:
                query=f"UPDATE Users SET password = '{new_password}' WHERE id_user = '{session['id']}'"
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash('Change made',"success")
                return redirect(url_for('profile_teacher'))
        return render_template("change_password.html",form = form,link1='/teacher',link2='/teacher/profile')
    return redirect(url_for('login'))
            

@app.route("/student/profile/changepassword",methods=["GET","POST"])

def changepassword_student():
    form=ChangepasswordForm()
    if 'loggedin' in session and session['role']=='student': 
        if(request.method == "POST" and form.validate_on_submit()):
            personnal_information = form.__dict__
            old_password=personnal_information["old_password"].data
            new_password=personnal_information["new_password"].data
            old_password=old_password.strip()
            new_password=new_password.strip()
            query=f"SELECT password FROM Users where id_user='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            res=cur.fetchone()
            if res['password'].strip()!=old_password:
                cur.close()
                flash('Wrong old password',"danger")
            else:
                query=f"UPDATE Users SET password = '{new_password}' WHERE id_user = '{session['id']}'"
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash('Change made',"success")
                return redirect(url_for('profile_student'))
        return render_template("change_password.html",form = form,link1='/student',link2='/student/profile')
    return redirect(url_for('login'))
            

@app.route("/teacher/profile/changemail",methods=["GET","POST"])

def changemail_teacher():
    
    form=ChangemailForm()
    if 'loggedin' in session and session['role']=='teacher': 
        if(request.method == "POST" and form.validate_on_submit()):
            personnal_information = form.__dict__
            old_mail=personnal_information["old_mail"].data
            new_mail=personnal_information["new_mail"].data
            old_mail=old_mail.strip()
            new_mail=new_mail.strip()
            query=f"SELECT email FROM Users where id_user='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            res=cur.fetchone()
            if res['email'].strip()!=old_mail:
                cur.close()
                flash('Wrong old email',"danger")
            else:
                cur2=db.connection.cursor()
                query="SELECT u.email,o.email,a.email FROM Users u INNER JOIN Schools s ON s.id_school=u.Schools_id_school INNER JOIN Operators o ON s.Operators_id_operators=o.id_operators INNER JOIN Administrator a ON s.Administrator_id_admin=a.id_admin"
                cur2.execute(query)
                list_mail=[i[0] for i in cur2.fetchall()]  
                cur2.close()
                if new_mail in list_mail:
                    cur.close()
                    error_email="Mail already exists"
                    flash(error_email,"danger")
                else:
                    query=f"UPDATE Users SET email = '{new_mail}' WHERE id_user = '{session['id']}'"
                    cur.execute(query)
                    db.connection.commit()
                    cur.close()
                    flash('Change made',"success")
                    return redirect(url_for('profile_teacher'))
        return render_template("change_mail.html",form = form,link1='/teacher',link2='/teacher/profile')
    return redirect(url_for('login'))


@app.route("/reserve/<int:ISBN>", methods = ["POST"])

def reserveBook(ISBN): 
    if 'loggedin' in session and (session['role']=='teacher'or session['role']=='student'): 
        query1=f"CALL Borrow_Or_Reserve('{ISBN}','{session['id']}',@location)"
        query2="SELECT @location"
        try:
            cur = db.connection.cursor()
            cur.execute(query1)
            db.connection.commit()
            cur.execute(query2)
            a=cur.fetchone()
            if a[0]=="Borrow":
                cur.close()
                flash("Book borrowed","success")
            else:
                cur.close()
                flash("Book reserved","success")
        except :
            flash("Request already done", "danger")
        if session['role']=="teacher":
            return redirect(url_for("teacher"))
        else:
            return redirect(url_for("student"))
    return redirect(url_for('login'))
        

@app.route("/see_review/<int:ISBN>")

def seeReviewBook(ISBN): 
    if 'loggedin' in session and (session['role']=='teacher'or session['role']=='student'):  
        query=f"SELECT grade, comment FROM Review where Books_ISBN='{ISBN}'"
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            column_names=[i[0] for i in cur.description]
            res=[dict(zip(column_names,entry))for entry in cur.fetchall()]
            query=f"SELECT title FROM Books where ISBN='{ISBN}'"
            cur.execute(query)
            a=cur.fetchone()
            cur.close()
            title=f"Reviews of {a[0]}"
            if session['role']=='teacher':
                return render_template("see_review_book.html",res=res,title=title,link1='/teacher',link2='/teacher/profile')
            else:
                return render_template("see_review_book.html",res=res,title=title,link1='/student',link2='/student/profile')
        except Exception as e:
            flash(str(e), "danger")
    return redirect(url_for('login'))


@app.route("/teacher/profile/review/<int:ISBN>", methods = ["POST"])

def review_book_teacher(ISBN):
    if 'loggedin' in session and session['role']=='teacher': 
        form = ReviewForm() 
        review_data = form.__dict__
        grade = review_data['grade'].data
        review = review_data['review'].data
        if form.validate_on_submit():
            query = f"INSERT INTO Review (Users_id_user,Books_ISBN,date,grade,comment,approved) VALUES ('{session['id']}', '{ISBN}',DATE(NOW()), '{grade}','{review}' , 0);"
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Review sent", "success")
            except:
                flash("Request already done", "danger")
        return redirect(url_for('profile_teacher'))
    return redirect(url_for('login'))
    

@app.route("/student/profile/review/<int:ISBN>", methods = ["POST"])

def review_book_student(ISBN):
    if 'loggedin' in session and session['role']=='student': 
        form = ReviewForm() 
        review_data = form.__dict__
        grade = review_data['grade'].data
        review = review_data['review'].data
        if form.validate_on_submit():
            query = f"INSERT INTO Review (Users_id_user,Books_ISBN,date,grade,comment,approved) VALUES ('{session['id']}', '{ISBN}',DATE(NOW()), '{grade}','{review}' , 0);"
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Review sent", "success")
            except:
                flash("Request already done", "danger")
        return redirect(url_for('profile_student'))
    return redirect(url_for('login'))


@app.route("/operator")

def operator():
    if 'loggedin' in session and session['role']=='operator':
        query=f"SELECT br.Books_ISBN ISBN,u.id_user id_user,u.first_name first_name, u.last_name last_name, DATEDIFF(DATE(NOW()), DATE_ADD(br.start_date, INTERVAL 7 DAY)) AS delayed_days FROM Users u  INNER JOIN Borrow br ON br.Users_id_user = u.id_user INNER JOIN Schools s ON s.id_school = u.Schools_id_school WHERE (br.end_date IS NULL) AND (DATE_ADD(br.start_date, INTERVAL 7 DAY) < DATE(NOW())) AND (s.Operators_id_operators ='{session['id']}') AND br.approved=1"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        a=cur.fetchone()
        title=f"In {a['school_name']} school, latecomers are:"
        cur.close()
        return render_template('landing_operator.html',title=title,res=res) 
    return redirect(url_for('login'))


@app.route("/operator/reservation" )

def manage_reservation():
    if 'loggedin' in session and session['role']=='operator': 
        query=f"SELECT r.Users_id_user id_user, r.Books_ISBN ISBN, r.date date, u.Roles_role role, IF (r.Users_id_user IN (SELECT Users_id_user FROM reserve WHERE approved = 1), (SELECT COUNT(Users_id_user) FROM reserve WHERE (approved = 1) AND Users_id_user = r.Users_id_user GROUP BY Users_id_user), 0) Books_already_reserved, IF(r.Users_id_user IN (SELECT id_user FROM books_borrowed GROUP BY id_user), (SELECT COUNT(bb.id_user) FROM books_borrowed bb WHERE r.Users_id_user = bb.id_user GROUP BY id_user), 0) Books_already_borrowed, IF (r.Users_id_user IN (SELECT id_user FROM books_borrowed WHERE DATE_ADD(start_date, INTERVAL 7 DAY) < DATE(NOW()) GROUP BY id_user), (SELECT COUNT(id_user) FROM Books_borrowed WHERE DATE_ADD(start_date, INTERVAL 7 DAY) < DATE(NOW()) AND id_user = r.Users_id_user GROUP BY id_user), 0) Books_delayed FROM Reserve r INNER JOIN Users u ON u.id_user = r.Users_id_user INNER JOIN Schools s ON s.id_school = u.Schools_id_school WHERE (r.approved = 0) AND (s.Operators_id_operators = '{session['id']}') GROUP BY r.Users_id_user, r.Books_ISBN, r.date, r.approved"          
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('manage_reservation.html',res=res)
    return redirect(url_for('login'))

@app.route("/operator/reservation/accept/<int:id_user>/<int:ISBN>",methods=["POST"])

def validate_reservation(ISBN,id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"UPDATE Reserve SET approved = 1, date=DATE(NOW()) WHERE (Users_id_user = '{id_user}' AND Books_ISBN = '{ISBN}' AND approved = 0);"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Reservation approved","success")
        return redirect(url_for('manage_reservation'))
    return redirect(url_for('login'))

@app.route("/operator/reservation/reject/<int:id_user>/<int:ISBN>",methods=["POST"])

def reject_reservation(ISBN,id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"DELETE FROM Reserve WHERE (Users_id_user = '{id_user}' AND Books_ISBN = '{ISBN}' AND approved = 0);"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Reservation rejected","success")
        return redirect(url_for('manage_reservation'))
    return redirect(url_for('login'))


@app.route("/operator/borrow" )

def manage_borrow():
    if 'loggedin' in session and session['role']=='operator': 
        query=f" SELECT bd.Users_id_user id_user, bd.Books_ISBN ISBN, bd.start_date start_date, u.Roles_role role, IF (bd.Users_id_user IN (SELECT Users_id_user FROM Reserve WHERE approved = 1 GROUP BY id_user), (SELECT COUNT(Users_id_user) FROM Reserve WHERE approved = 1 AND Users_id_user = bd.Users_id_user), 0) Books_already_reserved, IF (bd.Users_id_user IN (SELECT id_user FROM books_borrowed GROUP BY id_user), (SELECT COUNT(bb.id_user) FROM books_borrowed bb WHERE bd.Users_id_user = bb.id_user GROUP BY id_user), 0) Books_already_borrowed, IF (bd.Users_id_user IN (SELECT id_user FROM books_borrowed WHERE DATE_ADD(start_date, INTERVAL 7 DAY) < DATE(NOW()) GROUP BY id_user), (SELECT COUNT(id_user) FROM Books_borrowed WHERE DATE_ADD(start_date, INTERVAL 7 DAY) < DATE(NOW()) AND id_user = bd.Users_id_user GROUP BY id_user), 0) Books_delayed FROM borrow_demand bd INNER JOIN Users u ON u.id_user = bd.Users_id_user INNER JOIN Schools s ON s.id_school = u.Schools_id_school WHERE s.Operators_id_operators = '{session['id']}'"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('manage_borrow.html',res=res)
    return redirect(url_for('login'))

@app.route("/operator/borrow/accept/<int:id_user>/<int:ISBN>",methods=["POST"])

def validate_borrow(ISBN,id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"UPDATE Borrow SET approved = 1 , start_date=DATE(NOW()) WHERE (Users_id_user = '{id_user}' AND Books_ISBN = '{ISBN}' AND approved = 0);"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Borrow approved","success")
        return redirect(url_for('manage_borrow'))
    return redirect(url_for('login'))

@app.route("/operator/borrow/reject/<int:id_user>/<int:ISBN>",methods=["POST"])

def reject_borrow(ISBN,id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"DELETE FROM Borrow WHERE (Users_id_user = '{id_user}' AND Books_ISBN = '{ISBN}' AND approved = 0);"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Borrow rejected","success")
        return redirect(url_for('manage_borrow'))
    return redirect(url_for('login'))


@app.route("/operator/review" )

def manage_review():
    if 'loggedin' in session and session['role']=='operator': 
        query=f"SELECT r.Users_id_user id_user, CONCAT(u.first_name,' ', u.last_name) name, r.Books_ISBN ISBN, r.date date, r.grade grade, r.comment comment FROM Review r INNER JOIN Users u ON r.Users_id_user = u.id_user INNER JOIN Schools s ON u.Schools_id_school = s.id_school WHERE r.approved = 0 AND s.Operators_id_operators = '{session['id']}' "
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('manage_review.html',res=res)
    return redirect(url_for('login'))

@app.route("/operator/review/accept/<int:id_user>/<int:ISBN>",methods=["POST"])

def validate_review(ISBN,id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"UPDATE Review SET approved = 1 , date=DATE(NOW()) WHERE (Users_id_user = '{id_user}' AND Books_ISBN = '{ISBN}' AND approved = 0);"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Review approved","success")
        return redirect(url_for('manage_review'))
    return redirect(url_for('login'))

@app.route("/operator/review/reject/<int:id_user>/<int:ISBN>",methods=["POST"])

def reject_review(ISBN,id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"DELETE FROM Review WHERE (Users_id_user = '{id_user}' AND Books_ISBN = '{ISBN}' AND approved = 0);"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Review rejected","success")
        return redirect(url_for('manage_review'))
    return redirect(url_for('login'))

@app.route("/operator/books", methods=["GET","POST"])

def book_operator():
    form=Search_op_Form()
    if 'loggedin' in session and session['role']=='operator':
        if(request.method == "POST" and form.validate_on_submit()):
           book_information = form.__dict__
           book_title=book_information["title"].data
           book_category=book_information["category"].data
           book_author=book_information["author"].data
           book_copies=book_information["copies"].data
           book_title=book_title.strip()
           book_category=book_category.strip()
           book_author=book_author.strip()
           if book_copies is None:
               book_copies=''
           else:
               book_copies=book_copies
           try:
               query=f"SELECT b.ISBN ISBN,b.title title, b.number_of_pages number_pages, b.language language, b.summary summary, b.keywords keywords, cb.Categories_category_name category FROM Books b INNER JOIN Authors_Books ab ON ab.Books_ISBN = b.ISBN INNER JOIN Authors a ON a.id_author = ab.Authors_id_author INNER JOIN (SELECT Books_ISBN, GROUP_CONCAT(Categories_category_name) Categories_category_name FROM Categories_Books GROUP BY Books_ISBN) cb ON cb.Books_ISBN = b.ISBN INNER JOIN Schools s ON s.id_school = b.Schools_id_school  WHERE s.Operators_id_operators = '{session['id']}' AND  CASE WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' != '' AND '{book_copies}' != '')  THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%'))   WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' != '' AND '{book_copies}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%'))WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' = '' AND '{book_copies}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' != '' AND '{book_copies}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' != '' AND '{book_copies}' != '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' != '' AND '{book_copies}' = '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE( a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' = '' AND '{book_copies}' != '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' != '' AND '{book_category}' != '' AND '{book_author}' = '' AND '{book_copies}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' != '' AND '{book_copies}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' = '' AND '{book_copies}' != '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' != '' AND '{book_copies}' != '') THEN (UCASE(a.last_name) LIKE UCASE('%{book_author}%') AND UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' != '' AND '{book_category}' = '' AND '{book_author}' = '' AND '{book_copies}' = '') THEN (UCASE(b.title) LIKE UCASE('%{book_title}%')) WHEN ('{book_title}' = '' AND '{book_category}' != '' AND '{book_author}' = '' AND '{book_copies}' = '') THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{book_category}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' != '' AND '{book_copies}' = '') THEN (UCASE(a.last_name) LIKE UCASE('%{book_author}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' = '' AND '{book_copies}' != '') THEN (UCASE(b.available_copies) LIKE UCASE('%{book_copies}%')) WHEN ('{book_title}' = '' AND '{book_category}' = '' AND '{book_author}' = '' AND '{book_copies}' = '') THEN 1 END"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
               cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
               cur.execute(query)
               a=cur.fetchone()
               cur.close()
               title=f"Books in {a['school_name']} school:"
               return render_template('books_operator.html',res=res,title=title,form=form)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query=f"SELECT b.ISBN ISBN,b.title title, b.number_of_pages number_pages, b.language language, b.summary summary, b.keywords keywords, cb.Categories_category_name category FROM Books b  INNER JOIN (SELECT Books_ISBN, GROUP_CONCAT(Categories_category_name) Categories_category_name FROM Categories_Books GROUP BY Books_ISBN) cb ON cb.Books_ISBN = b.ISBN INNER JOIN Schools s ON s.id_school = b.Schools_id_school  WHERE s.Operators_id_operators = '{session['id']}' "    
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            a=cur.fetchone()
            cur.close()
            title=f"Books in {a['school_name']} school:"
            return render_template('books_operator.html',res=res,title=title,form=form)
    return redirect(url_for('login'))

@app.route("/operator/books/add" , methods=["GET","POST"])
def add_book():
    form=add_book_Form()  
    if 'loggedin' in session and session['role']=='operator': 
        if(request.method == "POST" and form.validate_on_submit()):
            book_information = form.__dict__
            ISBN=book_information["ISBN"].data
            title=book_information["title"].data
            publication_date=book_information["publication_date"].data
            publisher=book_information["publisher"].data
            number_pages=book_information["number_of_pages"].data
            summary=book_information["summary"].data
            available_copies=book_information["available_copies"].data
            language=book_information["language"].data
            keywords=book_information["keywords"].data
            first_name=book_information["first_name"].data
            last_name=book_information["last_name"].data
            category=book_information["category"].data
            cur=db.connection.cursor()
            try:
                query=f"SELECT id_school From Schools where Operators_id_operators='{session['id']}'"
                cur.execute(query)
                a=cur.fetchone()
                query=f"INSERT INTO Books (ISBN,title,publication_date,publisher,number_of_pages,summary,available_copies,language,keywords,Schools_id_school) VALUES ('{ISBN}', '{title}', '{publication_date}', '{publisher}', '{number_pages}', '{summary}','{available_copies}', '{language}', '{keywords}', '{a[0]}');"
                cur.execute(query)
                db.connection.commit()
                query=f"INSERT INTO Authors_Books (Books_ISBN,Authors_id_author) VALUES ('{ISBN}', (SELECT id_author FROM authors WHERE first_name = '{first_name}' AND last_name = '{last_name}')); "
                cur.execute(query)
                db.connection.commit()
                query=f"INSERT INTO Categories_Books (Books_ISBN,Categories_category_name) VALUES ('{ISBN}','{category}');"
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Book added","success")
            except:
                flash("Information unknown","danger")
            return redirect(url_for("book_operator"))
        return render_template("add_book.html",form = form)
    return(redirect(url_for("login")))
            

@app.route("/operator/book_return" , methods=["GET","POST"])

def return_book():
    form=return_book_Form()  
    if 'loggedin' in session and session['role']=='operator': 
        if(request.method == "POST" and form.validate_on_submit()):
            return_information = form.__dict__
            id_user=return_information['id_user'].data
            ISBN=return_information["ISBN"].data
            query=f"INSERT INTO Return_books (id_user, ISBN, end) VALUES ('{id_user}', '{ISBN}', DATE(NOW()));"
            cur=db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            flash("Book returned","success")
            return render_template("return_book.html",form = form)
        return render_template("return_book.html",form = form)
    return(redirect(url_for("login")))
    

@app.route("/operator/users", methods=["GET","POST"])

def check_user():
    form=check_user_Form()
    if 'loggedin' in session and session['role']=='operator':
        if(request.method == "POST" and form.validate_on_submit()):
           user_information = form.__dict__
           first_name=user_information['first_name'].data
           last_name=user_information['last_name'].data
           first_name=first_name.strip()
           last_name=last_name.strip()
           try:
               query=f"SELECT u.id_user id_user, CONCAT(u.first_name,' ' ,u.last_name) name,u.username username,u.birth_date date, u.approved approved, u.Roles_role role FROM Users u INNER JOIN Schools s ON u.Schools_id_school = s.id_school WHERE s.Operators_id_operators = '{session['id']}' AND CASE  WHEN '{first_name}' != '' AND '{last_name}' != '' THEN (UCASE(first_name) LIKE UCASE('{first_name}') AND UCASE(last_name) LIKE UCASE('{last_name}')) WHEN '{first_name}' = '' AND '{last_name}' != '' THEN (UCASE(last_name) LIKE UCASE('{last_name}')) WHEN '{first_name}' != '' AND '{last_name}' = '' THEN (UCASE(first_name) LIKE UCASE('{first_name}') )WHEN ('{first_name}'= '' AND '{last_name}' = '') THEN 1 END"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
               cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
               cur.execute(query)
               a=cur.fetchone()
               cur.close()
               title=f"Users in {a['school_name']} school:"
               return render_template('check_user.html',title=title,res=res,form=form)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query=f"SELECT u.id_user id_user,  CONCAT(u.first_name,' ' ,u.last_name) name,u.username username,u.birth_date date, u.approved approved, u.Roles_role role FROM Users u INNER JOIN Schools s ON u.Schools_id_school = s.id_school WHERE s.Operators_id_operators='{session['id']}'"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            a=cur.fetchone()
            cur.close()
            title=f"Users in {a['school_name']} school:"
            return render_template('check_user.html',title=title,res=res,form=form)
    return redirect(url_for('login'))
    

@app.route("/operator/users/reject/<int:id_user>",methods=["POST"])

def reject_user(id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"UPDATE Users set approved=0 WHERE id_user = '{id_user}';"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("User disapproved","success")
        return redirect(url_for('check_user'))
    return redirect(url_for('login'))

@app.route("/operator/users/accept/<int:id_user>",methods=["POST"])

def accept_user(id_user):
    if 'loggedin' in session and session['role']=='operator': 
        query=f"UPDATE Users set approved=1 WHERE id_user = '{id_user}';"
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("User approved","success")
        return redirect(url_for('check_user'))
    return redirect(url_for('login'))


@app.route("/operator/book_rating", methods=["GET","POST"])

def rating_book():
    form=rating_book_Form()
    if 'loggedin' in session and session['role']=='operator':
        if(request.method == "POST" and form.validate_on_submit()):
           information = form.__dict__
           id_user=information['id_user'].data
           if id_user is None:
               id_user=''
           else:
               id_user=id_user
           category=information['category'].data
           category=category.strip()
           try:
               query=f"SELECT  AVG(r.grade) AS avg_grade  FROM Review r INNER JOIN Books b ON b.ISBN = r.Books_ISBN INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN INNER JOIN Schools s ON s.id_school = b.Schools_id_school  WHERE s.Operators_id_operators = '{session['id']}' AND  CASE WHEN ('{id_user}' != '' AND '{category}' != '' ) THEN (r.Users_id_user = '{id_user}' AND UCASE(cb.Categories_category_name) LIKE UCASE('%{category}%')) WHEN ('{id_user}' != '' AND '{category}' = '' ) THEN (r.Users_id_user = '{id_user}') WHEN ('{id_user}' = '' AND '{category}' != '' ) THEN (UCASE(cb.Categories_category_name) LIKE UCASE('%{category}%')) WHEN ('{id_user}' = '' AND '{category}' = '' ) THEN 1 END"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
               cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
               cur.execute(query)
               a=cur.fetchone()
               cur.close()
               title=f"Rating in {a['school_name']} school:"
               return render_template('rating_book.html',title=title,res=res,form=form)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query=f"SELECT  AVG(r.grade) AS avg_grade FROM Review r INNER JOIN Books b ON b.ISBN = r.Books_ISBN INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN INNER JOIN Schools s ON s.id_school = b.Schools_id_school  WHERE s.Operators_id_operators = '{session['id']}'" 
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            query=f"SELECT s.name school_name FROM Schools s INNER JOIN Operators o  ON s.Operators_id_operators=o.id_operators WHERE o.id_operators='{session['id']}'"
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            a=cur.fetchone()
            cur.close()
            title=f"Rating in {a['school_name']} school:"
            return render_template('rating_book.html',title=title,res=res,form=form)
    return redirect(url_for('login'))

@app.route("/admin")

def administrator():
    if 'loggedin' in session and session['role']=='administrator':
        return render_template('landing_admin.html')
    return redirect(url_for('login'))


@app.route("/admin/reader_teacher")

def reader_teacher():
    if 'loggedin' in session and session['role']=='administrator':
        query="SELECT CONCAT(u.first_name, ' ', u.last_name) teachers_names, COUNT(*) books_borrowed FROM Users u INNER JOIN Borrow b ON u.id_user = b.Users_id_user WHERE (u.birth_date > DATE_ADD(DATE(NOW()), INTERVAL -40 YEAR)) AND (u.Roles_role = 'teacher') GROUP BY u.id_user ORDER BY 'books_borrowed' DESC LIMIT 1;"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('reader_teacher.html',res=res)
    return redirect(url_for('login'))
    

@app.route("/admin/unlucky_author")

def unlucky_author():
    if 'loggedin' in session and session['role']=='administrator':
        query="SELECT CONCAT(a.first_name, ' ', a.last_name) authors_names FROM Authors a WHERE a.id_author NOT IN (SELECT distinct(a.id_author) FROM Authors a INNER JOIN Authors_Books ab ON a.id_author = ab.Authors_id_author INNER JOIN Books b ON ab.Books_ISBN = b.ISBN INNER JOIN Borrow br ON b.ISBN = br.Books_ISBN);"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('unlucky_author.html',res=res)
    return redirect(url_for('login'))
    

@app.route("/admin/top_3")

def top_3():
    if 'loggedin' in session and session['role']=='administrator':
        query="SELECT T.Categories categories, COUNT(T.Categories) borrowing_times FROM (SELECT br.Books_ISBN ISBN, GROUP_CONCAT(cb.Categories_category_name) Categories, br.start_date FROM Borrow br INNER JOIN Books b ON b.ISBN = br.Books_ISBN INNER JOIN Categories_Books cb ON cb.Books_ISBN = b.ISBN  WHERE br.Books_ISBN IN (SELECT Books_ISBN FROM categories_books GROUP BY Books_ISBN HAVING COUNT(Books_ISBN)=2) GROUP BY br.Books_ISBN, br.start_date) T GROUP BY T.Categories ORDER BY borrowing_times DESC  LIMIT 3"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('top_3.html',res=res)
    return redirect(url_for('login'))
    

@app.route("/admin/unproductive_author")

def unproductive_author():
    if 'loggedin' in session and session['role']=='administrator':
        query="SELECT CONCAT(a.first_name, ' ', a.last_name) authors_names, T.Nbr_books number_books FROM Authors a INNER JOIN (SELECT ab.Authors_id_author, COUNT(ab.Authors_id_author) AS Nbr_books FROM Authors_Books ab GROUP BY ab.Authors_id_author) T  ON T.Authors_id_author = a.id_author  WHERE T.Nbr_books <= (SELECT MAX(T.Nbr_books) - 5 FROM (SELECT ab.Authors_id_author, COUNT(ab.Authors_id_author) AS Nbr_books FROM Authors_Books ab GROUP BY ab.Authors_id_author) T);"
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template('unproductive_author.html',res=res)
    return redirect(url_for('login'))
    

@app.route("/admin/loans_school", methods=["GET","POST"])

def admin_loans_school():
    form=school_loans_Form()
    if 'loggedin' in session and session['role']=='administrator':
        if(request.method == "POST" and form.validate_on_submit()):
           information = form.__dict__
           month=information['month'].data
           if month is None:
               month=''
           else:
               month=month
           year=information['year'].data
           if year is None:
               year=''
           else:
               year=year
           try:
               query=f"SELECT s.name school, count(br.Books_ISBN) number_loans FROM Schools s INNER JOIN Books b ON b.Schools_id_school = s.id_school INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN WHERE  CASE WHEN('{year}'!='' AND '{month}'!='') THEN(YEAR(br.start_date) = '{year}' AND MONTH(br.start_date) = '{month}') WHEN('{year}'='' AND '{month}'!='') THEN(MONTH(br.start_date) = '{month}') WHEN('{year}'!='' AND '{month}'='') THEN(YEAR(br.start_date) = '{year}' ) WHEN('{year}'='' AND '{month}'='') THEN 1 END GROUP BY s.name"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               title="Number of loans "
               return render_template('admin_loans_school.html',res=res,form=form,title=title)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query="SELECT s.name school, count(br.Books_ISBN) number_loans FROM Schools s INNER JOIN Books b ON b.Schools_id_school = s.id_school INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN GROUP BY s.name"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            title="Number of loans per school"
            return render_template('admin_loans_school.html',res=res,form=form,title=title)
    return redirect(url_for('login'))

@app.route("/admin/loans_operators", methods=["GET","POST"])

def admin_loans_operator():
    form=operator_loans_Form()
    if 'loggedin' in session and session['role']=='administrator':
        if(request.method == "POST" and form.validate_on_submit()):
           information = form.__dict__
           year=information['year'].data
           if year is None:
               year=''
           else:
               year=year
           try:
               query=f"SELECT o.id_operators id_operator, CONCAT(o.first_name,' ' ,o.last_name) operator_name, COUNT(br.Books_ISBN) AS books_loaned FROM Operators o INNER JOIN Schools s ON s.Operators_id_operators = o.id_operators INNER JOIN Books b ON b.Schools_id_school = s.id_school INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN WHERE CASE WHEN('{year}'!='') THEN (YEAR(br.start_date) = '{year}') WHEN('{year}'='') THEN 1 END GROUP BY o.id_operators, o.first_name, o.last_name HAVING COUNT(br.Books_ISBN) > 20"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               title="Operators who have loaned more than 20 books"
               return render_template('admin_loans_operator.html',res=res,form=form,title=title)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query="SELECT o.id_operators id_operator, CONCAT(o.first_name,' ' ,o.last_name) operator_name, COUNT(br.Books_ISBN) AS books_loaned FROM Operators o INNER JOIN Schools s ON s.Operators_id_operators = o.id_operators INNER JOIN Books b ON b.Schools_id_school = s.id_school INNER JOIN Borrow br ON br.Books_ISBN = b.ISBN GROUP BY o.id_operators, o.first_name, o.last_name HAVING COUNT(br.Books_ISBN) > 20"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            title="Operators who have loaned more than 20 books"
            return render_template('admin_loans_operator.html',res=res,form=form,title=title)
    return redirect(url_for('login'))


@app.route("/admin/affiliation_category", methods=["GET","POST"])

def admin_affiliation_category():
    form=affiliation_category_Form()
    if 'loggedin' in session and session['role']=='administrator':
        if(request.method == "POST" and form.validate_on_submit()):
           information = form.__dict__
           category=information['category'].data
           category=category.strip()
           try:
               query=f"SELECT CONCAT(a.first_name, ' ', a.last_name) authors_names FROM Authors a INNER JOIN Authors_Books ab ON ab.Authors_id_author = a.id_author INNER JOIN Books b ON b.ISBN = ab.Books_ISBN INNER JOIN Categories_Books ca ON ca.Books_ISBN = b.ISBN WHERE CASE WHEN ('{category}'!='') THEN (UCASE(ca.Categories_category_name)=UCASE('{category}')) WHEN ('{category}'='') THEN 1 END GROUP BY a.id_author;"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res1 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               title1="Authors who belong to the category" 
               query=f"SELECT CONCAT(u.first_name, ' ', u.last_name) teachers_names FROM Users u INNER JOIN Borrow bor ON bor.Users_id_user = u.id_user INNER JOIN Books boo ON boo.ISBN = bor.Books_ISBN INNER JOIN Categories_Books cb ON cb.Books_ISBN = boo.ISBN  WHERE u.Roles_role = 'teacher' AND bor.start_date > DATE_ADD(DATE(NOW()), INTERVAL -1 YEAR) AND CASE WHEN ('{category}'!='') THEN (UCASE(cb.Categories_category_name)=UCASE('{category}')) WHEN ('{category}'='') THEN 1 END GROUP BY u.id_user"
               cur = db.connection.cursor()
               cur.execute(query)
               column_names = [i[0] for i in cur.description]
               res2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
               cur.close()
               title2="Teachers who have borrowed books from that category in the last year"
               return render_template('admin_affiliation_category.html',res1=res1,res2=res2,form=form,title1=title1,title2=title2)
           except Exception as e: 
               flash(str(e), "danger") 
        else:
            query="SELECT CONCAT(a.first_name, ' ', a.last_name) authors_names FROM Authors a INNER JOIN Authors_Books ab ON ab.Authors_id_author = a.id_author INNER JOIN Books b ON b.ISBN = ab.Books_ISBN INNER JOIN Categories_Books ca ON ca.Books_ISBN = b.ISBN GROUP BY a.id_author;"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res1 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            title1="Authors who belong to the category" 
            query="SELECT CONCAT(u.first_name, ' ', u.last_name) teachers_names FROM Users u INNER JOIN Borrow bor ON bor.Users_id_user = u.id_user INNER JOIN Books boo ON boo.ISBN = bor.Books_ISBN INNER JOIN Categories_Books cb ON cb.Books_ISBN = boo.ISBN  WHERE (u.Roles_role = 'teacher' AND bor.start_date > DATE_ADD(DATE(NOW()), INTERVAL -1 YEAR)) GROUP BY u.id_user;"
            cur = db.connection.cursor()
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            res2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            title2="Teachers who have borrowed books from that category in the last year"
            return render_template('admin_affiliation_category.html',res1=res1,res2=res2,form=form,title1=title1,title2=title2)
    return redirect(url_for('login'))


@app.route("/admin/add_operator", methods=["GET","POST"])

def add_operator():
    form=add_operator_Form()
    if 'loggedin' in session and session['role']=='administrator':
        if(request.method == "POST" and form.validate_on_submit()):
           personnal_information = form.__dict__
           first_name=personnal_information["first_name"].data
           last_name=personnal_information["last_name"].data
           birth_date=personnal_information["birth_date"].data
           email=personnal_information["email"].data
           username=personnal_information["username"].data
           password=personnal_information["password"].data
           try:
               query=f"INSERT into Operators (first_name,last_name,birth_date,email,username,password,role,approved) VALUES ('{first_name}','{last_name}','{birth_date}','{email}','{username}','{password}','operator',1)"
               cur = db.connection.cursor()
               cur.execute(query)
               db.connection.commit()
               cur.close()
               flash('Operator added','success')
               return redirect(url_for("administrator"))
           except Exception as e: 
               flash(str(e), "danger") 
        return render_template('add_operator.html',form=form)
    return redirect(url_for('login'))


@app.route("/admin/add_school", methods=["GET","POST"])

def add_school():
    form=add_school_Form()
    if 'loggedin' in session and session['role']=='administrator':
        if(request.method == "POST" and form.validate_on_submit()):
           school_information = form.__dict__
           name=school_information["name"].data
           address=school_information["address"].data
           city=school_information["city"].data
           phone_number=school_information["phone_number"].data
           email=school_information["email"].data
           director_name=school_information["director_name"].data
           id_admin=school_information["id_admin"].data
           id_operator=school_information["id_operator"].data   
           try:
               query=f"INSERT into Schools (name,address,city,phone_number,email,director_name,Administrator_id_admin,Operators_id_operators) VALUES ('{name}','{address}','{city}','{phone_number}','{email}','{director_name}','{id_admin}','{id_operator}')"
               cur = db.connection.cursor()
               cur.execute(query)
               db.connection.commit()
               cur.close()
               flash('School added','success')
               return redirect(url_for("administrator"))
           except Exception as e: 
               flash(str(e), "danger") 
        return render_template('add_school.html',form=form)
    return redirect(url_for('login'))
