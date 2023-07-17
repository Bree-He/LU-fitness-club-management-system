import mysql.connector
from flask import (Blueprint, flash, redirect, render_template, request, session, url_for)
import connect

dbconn = None
trainer_bp = Blueprint('trainer', __name__, template_folder='templates', static_folder='static')

def getCursor():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser, \
        password=connect.dbpass, host=connect.dbhost, \
        database=connect.dbname, autocommit=True)
        dbconn = connection.cursor()
        return dbconn
    else:
        return dbconn

@trainer_bp.route('/')
def index():
    username = session.get('username')
    cur = getCursor()
    cur.execute("SELECT first_name FROM trainers WHERE email = %s", (username,))
    welcome = cur.fetchone()
    return render_template("trainer.html",username=welcome[0])

@trainer_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@trainer_bp.route("/trainerdetails")
def trainerdetails():
    username = session.get('username') # Get username from session
    cur = getCursor()
    cur.execute("SELECT trainer_id, CONCAT(first_name, ' ', last_name) AS Name, dob AS DOB, \
                email AS Email, phone AS Phone, education AS Education, Expertise AS Expertise, \
                self_introduction AS Introduction FROM trainers \
                JOIN user ON trainers.email = user.username WHERE user.username = %s",(username,))
    trainerProfile_result = cur.fetchall()
    trainerProfileColumn_names = [desc[0] for desc in cur.description]
    
    grpClass = "SELECT class_name AS Class, class_date AS Date, start_time AS Start, end_time AS End, COUNT(b.member_id) AS Participants FROM class_schedule c \
               LEFT JOIN booking b ON c.schedule_id = b.class_id \
               WHERE trainer_id = %s \
               GROUP BY c.schedule_id \
               ORDER BY class_date, start_time"

    cur.execute(grpClass, (trainerProfile_result[0][0],))
    grpClass_result = cur.fetchall()
    grpClassColumn_names= [desc[0] for desc in cur.description]
    ptClass = "SELECT pt_class_name AS Class, avail_date AS Date, start_time AS Start, end_time AS End, CONCAT(m.first_name, ' ', m.last_name) AS Participant, b.member_id AS Infomation \
              FROM pt_class pt \
              LEFT JOIN pt_class_schedule b ON pt.pt_class_id = b.pt_class_id \
              LEFT JOIN pt_class_payment pay ON b.member_id = pay.member_id \
              LEFT JOIN members m ON pay.member_id = m.member_id \
              WHERE trainer_id = %s \
              GROUP BY pt.pt_class_id \
              ORDER BY avail_date, start_time"
    cur.execute(ptClass, (trainerProfile_result[0][0],))
    ptClass_result = cur.fetchall()
    ptClassColumn_names= [desc[0] for desc in cur.description]
    return render_template("trainerdetails.html", trainerProfile = trainerProfile_result, dbcols=trainerProfileColumn_names,grpClass=grpClass_result, grpCols=grpClassColumn_names, ptClass=ptClass_result ,ptCols=ptClassColumn_names)

@trainer_bp.route('profile/update', methods=('GET','POST'))
def update_profile():
    cur = getCursor()
    username = session.get('username')# Get the username from the session
    if request.method == 'GET':
        cur.execute("SELECT trainer_id,first_name,last_name, expertise AS Expertise, email AS Email, phone AS Phone, dob, education, self_introduction FROM trainers \
                    JOIN user ON trainers.email = user.username WHERE user.username = %s",(username,))
        trainerProfile = cur.fetchone()
        return render_template('profileupdate.html', trainerProfile=trainerProfile)
    
    ###########update username if user change email and give session the new username to keep using the system##########
    new_email = request.form.get("email")
    if new_email != username:    
        cur.execute("UPDATE user SET username = %s WHERE username = %s", (new_email, username))
    session['username'] = new_email
    ###########update username if user change email and give session the new username to keep using the system##########
    
    update_sql = 'UPDATE trainers SET expertise = %s, email = %s, phone = %s, education = %s, self_introduction = %s WHERE trainer_id = %s'
    form = request.form
    try:
        cur.execute(update_sql, (
            form.get('expertise'), 
            form.get('email'),
            form.get('phone'), 
            form.get('education'),
            form.get('self_introduction'),
            form.get('trainer_id')
            )
        )
        flash('Update profile successfully!')
    except Exception as e:
        print(e)
        flash('Update profile failed!')
    return redirect(url_for('trainer.trainerdetails'))

@trainer_bp.route("/trainee")
def trainee():
    cursor = getCursor()
    query_trainer_class_sql = """
    SELECT m.member_id, m.first_name, m.last_name, m.dob, m.email, m.phone, m.health_condition,
    pt.pt_class_name AS Class, pt.avail_date AS Date, com.comment, sch.training_id
    FROM members m
    LEFT JOIN pt_class_payment pay ON m.member_id = pay.member_id
    LEFT JOIN pt_class_schedule sch ON pay.pt_booking_id = sch.training_id
    LEFT JOIN trainer_comment com ON sch.training_id = com.training_id
    LEFT JOIN pt_class pt ON sch.pt_class_id = pt.pt_class_id
    LEFT JOIN trainers ON pt.trainer_id = trainers.trainer_id
    WHERE trainers.email =%s;
    """
    cursor.execute(query_trainer_class_sql, (session.get('username'),))
    trainees = cursor.fetchall()
    return render_template('trainee.html',trainees=trainees)

@trainer_bp.route('/trainee/comment',methods=('GET','POST'))
def trainee_comment():
    #get form details 
    training_id = request.form.get('trainingId')
    print(training_id)
    comment = request.form.get('comment')
    #update comment for trainee
    cursor = getCursor()
    cursor.execute(f'SELECT COUNT(training_id) FROM trainer_comment WHERE training_id="{training_id}"')
    count = cursor.fetchone()[0]
    if count == 0:
        sql = f'INSERT INTO trainer_comment (comment,training_id) VALUES ("{comment}","{training_id}")'
        msg = 'Add Comment successfully!'
    else:
        sql = f'UPDATE trainer_comment SET comment="{comment}" WHERE training_id="{training_id}"'
        msg = 'Update Comment successfully!'
    cursor.execute(sql)
    flash(msg)
    return redirect(url_for('trainer.trainee'))
