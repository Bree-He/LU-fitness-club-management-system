import mysql.connector
from flask import (Blueprint, flash, redirect, render_template, request, session, url_for)
import connect
import re
from datetime import datetime, timedelta
import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


dbconn = None
member_bp = Blueprint('member', __name__,template_folder='templates', static_folder='static')

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
# def autopay():
# if yes check the due date <= today due date +30 

def autopay():
    username = session.get('username')
    connection = getCursor()
    connection.execute("SELECT sub_duedate, auto_pay,member_id FROM members m WHERE m.email = %s;",(username,))
    list=connection.fetchone()
    autopay=list[1]
    if autopay=='yes':
        duedate=list[0]
        due_date = datetime.datetime.combine(duedate, datetime.datetime.min.time())
    
        # today
        current_date = datetime.datetime.now()
        delta = due_date - current_date
        days_left = delta.days + 1

        if days_left<= 7:
            memberid=list[2]
            current_date = datetime.datetime.now()
            connection.execute("INSERT INTO payment_detail (member_id, payment_date, payment_amount, payment_method, payment_status) VALUES (%s, %s, %s, %s, 'Successful');", (memberid, current_date, '30','auto',))
            
            sub_duedate_str = duedate.strftime('%Y-%m-%d')
            duedate_dt = datetime.datetime.strptime(sub_duedate_str, '%Y-%m-%d')
             # add 30 days to subdate
            new_duedatedt = duedate_dt + timedelta(days=30)
             # convert expdate to string
            new_duedate = new_duedatedt.strftime('%Y-%m-%d')
            connection.execute("UPDATE members set subscription_status=%s, sub_duedate = %s WHERE member_id = %s;",('active',new_duedate,memberid,))
        else:
            return True
    else:
        return True

def checkstatus():
    username = session.get('username')
    connection = getCursor()
    # change status first!!!
        
    connection.execute("SELECT sub_duedate, auto_pay FROM members m WHERE m.email = %s;",(username,))
    list=connection.fetchone()
    autopay=list[1]
    if autopay=='no':
        duedate=list[0]
        due_date = datetime.datetime.combine(duedate, datetime.datetime.min.time())
    
        # today
        current_date = datetime.datetime.now()
        delta = due_date - current_date
        days_left = delta.days + 1
        return days_left
    else: return 8
                      
@member_bp.route('/')
def index():
    # sub reminder straight away!!
    username = session.get('username')
    connection = getCursor()
    connection.execute("SELECT first_name FROM members WHERE email = %s", (username,))
    welcome = connection.fetchone()
    autopay()
    days_left=checkstatus()
    if days_left <0:
        # inactive  auto pay no!!
        connection.execute("UPDATE members SET subscription_status = 'inactive', auto_pay = 'no' WHERE email = %s;",(username,))
        message = 'Please renew your subscription!'
        
        return render_template("member.html",username=welcome[0],message=message)
    elif days_left <= 7:
        message="Membership is expiring soon! {} days left".format(days_left)
       
        return render_template("member.html",username=welcome[0],message=message)
    else:
         return render_template("member.html",username=welcome[0])
        
@member_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

######view the member's information --Bree
@member_bp.route("/profile")
def profile():
    username = session.get('username') # Get the username from the session
    connection = getCursor()
    connection.execute("SELECT members.member_id, members.first_name, members.last_name, members.dob, members.email, members.address, members.phone, \
                                members.health_condition, members.sub_duedate\
                        FROM members \
                        JOIN user ON members.email = user.username\
                        WHERE user.username = %s",(username,)) 
    member_profile = connection.fetchall()
    return render_template("profile.html", memberprofile=member_profile)

#######update the member's information--Bree
@member_bp.route("/profile/update/", methods=["POST"])
def profile_update():
    username = session.get('username') # Get the username from the session
    connection = getCursor()
    address = request.form.get("address")
    contact_number = request.form.get("phone")
    health_condition = request.form.get("health_condition")
    new_email = request.form.get("email")
    # Get the old email from the members table
    connection.execute("SELECT email FROM members WHERE email = %s",(username,))
    old_email = connection.fetchone()[0]
    # Check if the email has changed
    if new_email != old_email:     
        # Update the user table with the new email
        connection.execute("UPDATE user SET username = %s WHERE username = %s", (new_email, username))
        # Update the session with the new email
        session['username'] = new_email
    # Update the member's information using the username
    connection.execute("UPDATE members SET address = %s, phone = %s, health_condition = %s, email = %s WHERE email = %s",
                       (address, contact_number, health_condition, new_email, username))
    # Retrieve the updated member's information
    connection.execute("SELECT members.member_id, members.first_name, members.last_name, members.dob, members.email, members.address, members.phone, \
                                members.health_condition, members.sub_duedate\
                        FROM members \
                        JOIN user ON members.email = user.username\
                        WHERE user.username = %s",(new_email,)) 
    new_member_profile = connection.fetchall()
    # Set the success message
    success_message = "Your profile updated successfully"
    return render_template("profile.html", memberprofile = new_member_profile, success_message =success_message)

########view the exercise sessions--Bree
@member_bp.route("/sessions")
def sessions():
    connection = getCursor()
    sql = """SELECT class_schedule.class_name
            FROM class_schedule 
            GROUP BY class_schedule.class_name;""" 
    connection.execute(sql)
    sessions_list = connection.fetchall()   
    return render_template("group_class.html", sessionslist = sessions_list) # Render the sessions list to the "sessions.html" template

#####show the description of the class--Bree
@member_bp.route("/sessions/description")
def sdescription():
    class_name = request.args.get('class_name') # Get the class name from the URL parameter using the request object
    connection = getCursor()
    sql = f"""SELECT * FROM class_detail WHERE class_name = '{class_name}';"""  # Execute a query to get the description of the class using the class name
    connection.execute(sql)
    descriptions = connection.fetchall()
    return render_template("/sessions/description.html", descriptions = descriptions)    # Render the class description to the "description.html" template

#####view the trainers' list--Bree
@member_bp.route("/trainers")
def trainers():
    connection = getCursor()
    sql = """SELECT 
                trainers.trainer_id,
                CONCAT(trainers.first_name, ' ', trainers.last_name) AS trainername,
                class_schedule.class_day,
                MIN(class_schedule.start_time) AS start_time, 
                MAX(class_schedule.end_time) AS end_time, 
                class_schedule.class_name
            FROM 
                class_schedule
                INNER JOIN trainers ON class_schedule.trainer_id = trainers.trainer_id
            GROUP BY 
                class_schedule.class_name,
                trainers.trainer_id,
                trainers.first_name,
                trainers.last_name,
                class_schedule.class_day
            ORDER BY 
                trainers.first_name"""  
    connection.execute(sql)
    trainers_list = connection.fetchall()
    return render_template("trainers.html", trainerslist = trainers_list) # Render the trainers list to the "trainers.html" template

#####view the description of trainers--Bree
@member_bp.route("/trainers/description")
def tdescription():
    trainer_id = request.args.get('trainer_id') 
    connection = getCursor()
    # Get the trainer's profile
    sql = f"""SELECT * FROM trainers WHERE trainer_id = '{trainer_id}';"""
    connection.execute(sql)
    descriptions = connection.fetchall()
    trainer_name = f"{descriptions[0][1]} {descriptions[0][2]}"
    return render_template("/trainers/description.html", descriptions=descriptions, trainer_name=trainer_name)

#####view the my bookings of members--Bree
@member_bp.route("/bookings")
def bookings():
    username = session.get('username') # Get the username from the session
    connection = getCursor()
    connection.execute("select members.member_id, class_schedule.class_name, class_schedule.class_date, CONCAT(class_schedule.start_time, '-', class_schedule.end_time) AS classtime\
                        from members\
                        join booking on members.member_id = booking.member_id\
                        join class_schedule on booking.class_id = class_schedule.schedule_id\
                        join user on members.email = user.username\
                        where user.username = %s ORDER BY class_schedule.class_date",(username,)) 
    my_booking = connection.fetchall()
    connection.execute("select members.member_id, pt_class.pt_class_name, pt_class.avail_date,CONCAT(pt_class.start_time, '-', pt_class.end_time) AS classtime\
                        from members\
                        join pt_class_schedule on members.member_id = pt_class_schedule.member_id\
                        join pt_class on pt_class_schedule.pt_class_id = pt_class.pt_class_id\
                        join user on members.email = user.username\
                        where user.username = %s ORDER BY pt_class.avail_date",(username,)) 
    my_ptbooking = connection.fetchall()
    return render_template("bookings.html", mybooking=my_booking, myptbooking=my_ptbooking)

@member_bp.route('/pay')
def pay():
    # show user the due date
    username = session.get('username')
    connection = getCursor()
    connection.execute("SELECT m.sub_duedate FROM members m WHERE m.email = %s;",(username,)) 
    duedate= connection.fetchone()[0]
    
    return render_template("mem_payment.html",duedate= duedate)

# Na

@member_bp.route('/payment', methods=["POST"])
def payment():
     # username to get id first!!
    username = session.get('username')
    connection = getCursor()
    connection.execute("SELECT m.member_id FROM members m WHERE m.email = %s;",(username,)) 
    member_id= connection.fetchone()[0]
    payment_date = datetime.datetime.now().date()
    payment_amount = request.form.get('amount')
    payment_method = request.form.get('card_type')
    connection.execute("INSERT INTO payment_detail (member_id, payment_date, payment_amount, payment_method, payment_status) VALUES (%s, %s, %s, %s, 'Successful');", (member_id, payment_date, payment_amount,payment_method,))
    # update the auto pay in members table
    auto_pay = request.form.get('renewal')
    connection.execute("UPDATE members set auto_pay = %s WHERE member_id = %s;",(auto_pay,member_id,))
    connection.execute("SELECT subscription_status from members WHERE member_id = %s;",(member_id,))
    # tuple
    sub_status=connection.fetchone()[0]
    
    # check the sub status first!!!
    if sub_status == 'inactive':
        todaydate = datetime.datetime.now().date()
        # change to str
        todaydate_str = todaydate.strftime('%Y-%m-%d')
        # convert subdate to datetime object
        todaydate_dt = datetime.datetime.strptime(todaydate_str, '%Y-%m-%d')
        # add 30 days to subdate
        duedate_dt = todaydate_dt + timedelta(days=30)
        # convert expdate to string
        new_duedate = duedate_dt.strftime('%Y-%m-%d')
        # change sub status also!!!
        connection.execute("UPDATE members set subscription_status=%s, sub_duedate = %s WHERE member_id = %s;",('active',new_duedate,member_id,))
        connection.execute("Select m.member_id, p.payment_date, p.payment_amount, p.payment_status, m.subscription_status, m.sub_duedate  from payment_detail p join members m WHERE payment_date =%s and m.member_id=%s;",(payment_date,member_id,))
        paybill= connection.fetchone()

        return render_template("payment.html", paybill=paybill)
    else:
    # add 30 days to due date in member table
        connection.execute("SELECT sub_duedate from members WHERE member_id = %s;",(member_id,))
    # tuple   datetime.date
        sub_duedate= connection.fetchone()[0]
    # change to str
        sub_duedate_str = sub_duedate.strftime('%Y-%m-%d')
        duedate_dt = datetime.datetime.strptime(sub_duedate_str, '%Y-%m-%d')
    # add 30 days to subdate
        new_duedatedt = duedate_dt + timedelta(days=30)
    # convert expdate to string
        new_duedate = new_duedatedt.strftime('%Y-%m-%d')
        connection.execute("UPDATE members set sub_duedate = %s WHERE member_id = %s;",(new_duedate,member_id,))

    # get the info from payment table
        connection.execute("Select m.member_id, p.payment_date, p.payment_amount, p.payment_status, m.subscription_status,m.sub_duedate  from payment_detail p join members m WHERE payment_date =%s and m.member_id=%s;",(payment_date,member_id,))
        # pay on same day take last pay
        paybill= connection.fetchall()[-1]

        return render_template("payment.html", paybill=paybill)
    


#23 Frank Personal training session searching, booking and payment function

class SearchForm(FlaskForm):
        pt_class_name = SelectField('pt_class_name', choices=[], validators=[DataRequired()])
        first_name = SelectField('first_name', choices=[], validators=[DataRequired()])
        avail_date = SelectField('avail_date', choices=[], validators=[DataRequired()])
    
# Define routes
@member_bp.route('/ptsearch', methods=['GET', 'POST'])
def ptsearch():
    form = SearchForm()
    connection = getCursor()
    # Get pt_class_name options from database
    connection.execute("SELECT DISTINCT pt_class_name FROM pt_class ORDER BY pt_class_name")
    pt_class_names = connection.fetchall()
    form.pt_class_name.choices = [('all', 'All')] + [(pt_class_name[0], pt_class_name[0]) for pt_class_name in pt_class_names]
    
    # Get trainer options from database
    connection.execute("SELECT DISTINCT first_name FROM trainers ORDER BY first_name")
    first_names = connection.fetchall()
    form.first_name.choices = [('all', 'All')] + [(first_name[0], first_name[0]) for first_name in first_names]
    
    # Get avail_date options from database
    connection.execute("SELECT DISTINCT avail_date FROM pt_class WHERE pt_class.avail_date > CURRENT_DATE() ORDER BY pt_class.avail_date")
    avail_dates = connection.fetchall()
    form.avail_date.choices = [('all', 'All')] + [(avail_date[0], avail_date[0]) for avail_date in avail_dates]

    # Set default values for search parameters
    pt_class_name = 'all'
    first_name = 'all'
    avail_date = 'all'

    if form.validate_on_submit():
        # Get search parameters
        pt_class_name = request.form.get('pt_class_name')
        first_name = request.form.get('first_name')
        avail_date = request.form.get('avail_date')
        
    # Generate SQL query with search parameters
    if  pt_class_name == 'all':
        pt_class_name_query = ''
    else:
        pt_class_name_query = "pt_class_name = '{}' AND".format(pt_class_name)

    if  first_name == 'all':
        first_name_query = ''
    else:
        first_name_query = "first_name = '{}' AND".format(first_name)

    if not avail_date:
       avail_date_query = "avail_date >= '1900-01-01'"
    elif avail_date == 'all':
       avail_date_query = "avail_date >= '1900-01-01'"
    else:
       avail_date_query = "avail_date = '{}'".format(avail_date)

    #Show all results meet the searching criteria
    query = "SELECT pt_class.pt_class_name, trainers.first_name, pt_class.avail_date, pt_class.start_time, pt_class.end_time, pt_class.price, pt_class.pt_class_id\
             FROM pt_class \
             JOIN trainers ON pt_class.trainer_id = trainers.trainer_id \
             WHERE {} {} {} \
             AND pt_class.capacity != 0 \
             AND pt_class.avail_date > CURRENT_DATE() \
             ORDER BY pt_class.avail_date, pt_class.start_time ".format(pt_class_name_query, first_name_query, avail_date_query)
             


    # Execute query and get results
    connection.execute(query)
    results = connection.fetchall()
    return render_template('ptsearch.html', form=form, results=results)



# personal training payment route

@member_bp.route('/ptsearch/pt_payment', methods=['GET','POST'])
def pt_payment():
    username = session.get('username')
    connection = getCursor()
    #get member id
    connection.execute("SELECT m.member_id, m.sub_duedate FROM members m WHERE m.email = %s;",(username,)) 
    result = connection.fetchone()
    member_id = result[0]
    sub_duedate = result[1]

    if sub_duedate >= datetime.datetime.now().date():
    
    #get payment date as today
      pt_class_payment_date = datetime.datetime.now().date()
    #get personal training class id
      pt_class_id = request.form.get('pt_class_id')
      connection.execute ("SELECT price FROM pt_class WHERE pt_class_id = %s;", (pt_class_id,))
      pt_class_payment_amount = connection.fetchone()[0]
    #insert all information to the tables
      connection.execute("INSERT INTO pt_class_payment (member_id, pt_class_payment_date, pt_class_payment_amount, pt_class_payment_method, pt_class_payment_status) VALUES (%s, %s, %s, 'Online', 'Successful');", (member_id, pt_class_payment_date, pt_class_payment_amount,))
      connection.execute("INSERT INTO pt_class_schedule (member_id, pt_class_id) VALUES (%s, %s);", (member_id, pt_class_id,))
      connection.execute("SELECT LAST_INSERT_ID()")
      training_id = connection.fetchone()[0]
      connection.execute("UPDATE pt_class_payment SET pt_booking_id = %s where payment_id = (SELECT tmp.payment_id FROM (SELECT MAX(payment_id) AS payment_id FROM pt_class_payment) AS tmp) ;" ,(training_id, ))
      connection.execute("UPDATE pt_class SET capacity = 0 WHERE pt_class_id = %s;", (pt_class_id,))
      results=connection.fetchall()
    #update attendance table, assuming the attendance date is the training date
      connection.execute("SELECT avail_date from pt_class where pt_class_id = %s;", (pt_class_id,))
      attendance_date = connection.fetchone()[0]
      connection.execute("INSERT INTO attendance (member_id, attendance_date, attendance_type, pt_booking_id) VALUE (%s,%s,'2',%s );", (member_id, attendance_date, training_id,))
      return render_template('pt_payment.html', results=results)
    else:
        flash("Your membership status is inactive, please subscribe your membership first before booking personal training sessions!")
        return redirect(url_for('member.pay'))

@member_bp.route('/ptsearch/pt_payment_success', methods=['GET','POST'])
def pt_payment_success():  
    connection = getCursor()
    connection.execute("SELECT pt_class.pt_class_id, pt_class.pt_class_name, pt_class.avail_date, pt_class.start_time, pt_class_schedule.pt_class_id, pt_class_schedule.training_id FROM pt_class Inner Join pt_class_schedule on pt_class.pt_class_id = pt_class_schedule.pt_class_id ORDER BY pt_class_schedule.training_id DESC LIMIT 1;",)
    results=connection.fetchall()
    flash("Thanks for your payment!")
    return render_template('pt_payment_success.html', results=results)



# view the all classes
@member_bp.route("/class/list")
def class_list():
    connection = getCursor() 
    sql = """SELECT class_name
            FROM class_schedule
            GROUP BY class_name
            ORDER BY class_name"""
    connection.execute(sql)
    class_list = connection.fetchall()
    return render_template("all_class.html", class_list=class_list)

@member_bp.route("/class/book", methods=('GET', 'POST'))
def book_class():
    connection = getCursor()
    email = session.get('username')
    connection.execute("SELECT subscription_status, member_id FROM members WHERE email = %s", (email,))
    result = connection.fetchone()
    subStatus = result[0]
    member_id = result[1]

    if subStatus != "active":
        flash("Please renew your membership before booking!", "error")
        return redirect(url_for('member.pay'))
    
    class_name = request.args.get('class_name')
    weekday = request.args.get('weekday')

    if request.method == 'POST':
        class_date = request.form.get('book_time')

        if class_date == None:
            flash('Please choose the date.', "warning")
            return redirect(request.referrer)
        else:
            findingClassId = "SELECT schedule_id FROM class_schedule \
                            WHERE class_name = %s AND class_date = %s"
            connection.execute(findingClassId, (class_name, class_date))
            schedule_id = connection.fetchone()[0]
            checkIfDoubleBooked = f"SELECT COUNT(b.member_id), cs.class_date FROM booking b \
                                   JOIN class_schedule cs ON b.class_id = cs.schedule_id \
                                   WHERE b.member_id= '{member_id}' AND cs.schedule_id = '{schedule_id}'"
            checkIfClassIsFull = f"SELECT max_capacity FROM class_schedule \
                                  WHERE class_name = '{class_name}' AND class_date = '{class_date}'"
            connection.execute(checkIfDoubleBooked)
            doubleBooked = connection.fetchone()[0]
            connection.execute(checkIfClassIsFull)
            capacity = connection.fetchone()[0]

            if doubleBooked != 0:
                flash('You have alrady book the class for your selected date!', "warning")
                return redirect(request.referrer)
            elif capacity == 0:
                flash('The class for your selected date is full.', "warning")
                return redirect(request.referrer)
            else:
                updateClassCapacity = f"UPDATE class_schedule SET max_capacity = '{capacity}' - 1 \
                                        WHERE class_name = '{class_name}' AND class_date = '{class_date}'"
                connection.execute(updateClassCapacity)
                newBooking = 'INSERT INTO booking (member_id, class_id) VALUES (%s, %s)'
                connection.execute(newBooking, (member_id, schedule_id))
                flash('book class successfully!')
                return redirect(url_for('member.class_list')) 
    else:
        today = datetime.date.today()
        classDetail = f"""SELECT * FROM class_detail WHERE class_name = '{class_name}';"""
        classSchedule = f"""SELECT * FROM class_schedule WHERE class_name = '{class_name}' AND class_day='{weekday}' AND class_date >='{today}';"""
        connection.execute(classDetail)
        description = connection.fetchone()
        connection.execute(classSchedule)
        schedules = connection.fetchall()
        return render_template("book_class.html", description=description, schedules=schedules)
