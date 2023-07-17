import csv
import io
import re
from csv import writer

import mysql.connector
from flask import (Blueprint, Response, flash, redirect, render_template,
                   request, session, url_for)

import connect
from datetime import datetime, timedelta
import calendar
import datetime
dbconn = None
admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

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

def checkstatus():
    connection = getCursor()
    connection.execute("SELECT member_id, sub_duedate FROM members;") 
    duelist=connection.fetchall()
    for list in duelist:
        duedate=list[1]
    # Convert the subscription due date to a datetime object
        duedate_str = duedate.strftime('%Y-%m-%d')
        duedate = datetime.datetime.strptime(duedate_str, '%Y-%m-%d')
        duedate = duedate.date()
    # Get today's date
        today = datetime.datetime.now()
        today_date = today.date()
        if duedate < today_date:
            connection.execute("UPDATE members SET subscription_status = 'inactive', auto_pay = 'no' where member_id=%s;",(list[0],))
    
    return True
def autopay():
    connection = getCursor()
    # change status first!!!
        
    connection.execute("SELECT member_id, sub_duedate FROM members m WHERE m.auto_pay='yes';")
    autolist=connection.fetchall()
    for list in autolist:
        duedate=list[1]
        memberid=list[0]
        due_date = datetime.datetime.combine(duedate, datetime.datetime.min.time())
    
        # today
        current_date = datetime.datetime.now()
        delta = due_date - current_date
        days_left = delta.days + 1
        if days_left <= 0:
            connection.execute("INSERT INTO payment_detail (member_id, payment_date, payment_amount, payment_method, payment_status) VALUES (%s, %s, %s, %s, 'Successful');", (memberid, current_date, '30','auto',))
            # add 30 days
            sub_duedate_str = duedate.strftime('%Y-%m-%d')
            duedate_dt = datetime.datetime.strptime(sub_duedate_str, '%Y-%m-%d')
             # add 30 days to subdate
            new_duedatedt = duedate_dt + timedelta(days=30)
             # convert expdate to string
            new_duedate = new_duedatedt.strftime('%Y-%m-%d')
            connection.execute("UPDATE members set subscription_status=%s, sub_duedate = %s WHERE member_id = %s;",('active',new_duedate,memberid,))
            
        else:
            return True




@admin_bp.route('/')
def index():
    username = session.get('username')
    
    autopay()
    checkstatus()
    return render_template("admin.html", username=username)

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

##########↓↓↓↓↓Special↓↓↓↓↓##########
def getAllTrainers(): # this funtion is repeated in bewlow codes, so I creat a funtion for ease my future use.
    cur = getCursor()
    cur.execute("SELECT trainer_id, CONCAT(first_name, ' ', last_name) AS Trainer FROM trainers ORDER BY Trainer;")
    trainer_result = cur.fetchall()
    return trainer_result

##########↓↓↓↓↓Special↓↓↓↓↓##########
def getTrainersClasses():
    cur = getCursor()
    sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
          FROM class_schedule AS class \
          JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
          ORDER BY Date, Start"
    cur.execute(sql)
    result = cur.fetchall()
    return result

##########↓↓↓↓↓Special↓↓↓↓↓##########
def getSubReport():
    cur = getCursor()
    sql = "SELECT member_id AS MemberId, CONCAT(first_name, ' ', last_name) AS Name, email AS Email, \
          subscription_status AS Status, auto_pay AS AutoPayment, sub_duedate AS MembershipDueDate FROM members ORDER BY member_id;"
    cur.execute(sql)
    result = cur.fetchall()
    return result

##########↓↓↓↓↓Special↓↓↓↓↓##########
def getSubStatus():
    cur = getCursor()
    cur.execute("SELECT DISTINCT subscription_status FROM members ORDER BY subscription_status;")
    result = cur.fetchall()
    return result

##########↓↓↓↓↓Special↓↓↓↓↓##########
def getDatesToWeekday(select_result):#Add weekday to result
    newListWithWeekday = []
    for classes in select_result:
        y, m, d = str(classes[2]).split('-')
        weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        result = calendar.weekday(int(y), int(m), int(d))
        newTurpleWithWeekday = classes + (weekday[result],)
        newListWithWeekday.append((newTurpleWithWeekday))
    return newListWithWeekday

##########↓↓↓↓↓Special↓↓↓↓↓##########
def getMonths():
    months =[('1','January',), ('2','February',), ('3','March',), ('4','April',), ('5','May',), ('6','June',)
             , ('7','July',), ('8','August',), ('9','September',), ('10','October',), ('11','November',), ('12','December',)]
    return months

@admin_bp.route('/addmember')
def addmember():
    todaydate = datetime.datetime.now().date()
    return render_template("addmember.html", subdate=todaydate)

def getmemberlist():
    connection = getCursor()
    connection.execute("SELECT * FROM members ORDER BY member_id DESC LIMIT 100;")
    memberList = connection.fetchall()
    return memberList

@admin_bp.route("/add_member", methods=["POST"])
def add_member():
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    dob = request.form.get('dob')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    health_condition = request.form.get('health_condition')

    subdate = request.form.get('subdate')
    # convert subdate to datetime object
    subdate_dt = datetime.datetime.strptime(subdate, '%Y-%m-%d')

    # add 30 days to subdate
    duedate_dt = subdate_dt + timedelta(days=30)

    # convert expdate to string
    duedate = duedate_dt.strftime('%Y-%m-%d')

    cur = getCursor()
    #  update user table!!!!
    cur.execute("SELECT email from members;")
    mem_email=cur.fetchall()
    for emaillist in mem_email:
        if email in emaillist:
            todaydate = datetime.datetime.now().date()
            msg="Email already exists!"
            return render_template("addmember.html", subdate=todaydate, msg=msg, firstname=first_name, lastname=last_name, dob=dob, address=address, email=email, phone=phone, health_condition=health_condition) 
    else:
        cur.execute("INSERT INTO user ( username, role) VALUES(%s,'member');",(email,))
        cur.execute("INSERT INTO members ( first_name, last_name, dob, address, email, phone,subscription_status, health_condition, sub_duedate) VALUES(%s,%s,%s,%s,%s,%s,'active',%s,%s);",(first_name, last_name, dob, address,email, phone, health_condition,duedate,))
    
    # get the lastest memberid
        member_id = cur.lastrowid
    # also update the payment for member
        cur.execute("INSERT INTO payment_detail(member_id, payment_date, payment_amount, payment_method, payment_status) VALUES(%s,%s,'0', 'signup', 'Successful');",(member_id,subdate,))
        memberList = getmemberlist()
        msg="New member added successfully"
        return  render_template("memberlist.html" ,memberlist = memberList, msg=msg)


@admin_bp.route("/search",methods=['GET','POST'])
def search():
    connection = getCursor()
    if request.method == 'POST':
        searchterm = request.form.get('search')
        searchterm = "%" + searchterm + "%"
        if request.form.get('searchtype')=="name":
            connection = getCursor()
            query = "SELECT * FROM members WHERE CONCAT(first_name, last_name) LIKE '" + searchterm + "'"
            connection.execute(query)
            memberlist = connection.fetchall()
            column_names = [desc[0] for desc in connection.description]
            if not memberlist:
              error_msg = "No results found, plese check the input."
              return render_template("search.html", error_msg=error_msg) 
            return render_template("search.html",memberlist=memberlist , column_names=column_names)
   
        elif request.form.get('searchtype')=="memberid":
            connection = getCursor()
            connection.execute("SELECT * FROM members WHERE member_id LIKE %s;", (searchterm,))
            memberlist = connection.fetchall()
            column_names = [desc[0] for desc in connection.description]
            if not memberlist:
            #   error when wrong input
              error_msg = "No results found, plese check the input."
              return render_template("search.html", error_msg=error_msg) 
            return render_template("search.html", memberlist=memberlist, column_names=column_names)
    else:
        memberlist = getmemberlist()
        column_names = [desc[0] for desc in connection.description]
        return render_template("search.html", memberlist=memberlist, column_names=column_names)
    
@admin_bp.route('/unsub/<int:memberid>')
def unsub(memberid):
    connection = getCursor()
    memberid = memberid 
    # change auto pay
    connection.execute("UPDATE members set subscription_status = 'inactive', auto_pay='No' where member_id=%s;",(memberid,))
    connection.execute("SELECT * FROM members WHERE member_id = %s;",(memberid,))
    member=connection.fetchall()
    column_names = [desc[0] for desc in connection.description]
    return render_template("editmember.html", member=member,column_names=column_names)

# add payment 
@admin_bp.route('/sub/<int:memberid>')
def sub(memberid):
    connection = getCursor()
    memberid = memberid 
    connection.execute("UPDATE members set subscription_status = 'active'where member_id=%s;",(memberid,))
    connection.execute("SELECT * FROM members WHERE member_id = %s;",(memberid,))
    member=connection.fetchall()
    column_names = [desc[0] for desc in connection.description]
    submsg="Member subscription status updated successfully"
    payment_date = datetime.datetime.now().date()
    # pay when inactive
    connection.execute("INSERT INTO payment_detail (member_id, payment_date, payment_amount, payment_method, payment_status) VALUES (%s, %s, %s, %s, 'Successful');", (memberid, payment_date, '30','at gym',))
    # update duedate
    # today + 30
    today = datetime.datetime.now()
    # change to str
    sub_duedate_str = today.strftime('%Y-%m-%d')
    duedate_dt = datetime.datetime.strptime(sub_duedate_str, '%Y-%m-%d')
    # add 30 days to subdate
    new_duedatedt = duedate_dt + timedelta(days=30)
    # convert expdate to string
    new_duedate = new_duedatedt.strftime('%Y-%m-%d')
    connection.execute("UPDATE members set sub_duedate = %s WHERE member_id = %s;",(new_duedate,memberid,))
    return render_template("editmember.html", member=member,column_names=column_names, submsg=submsg)

@admin_bp.route('/edit/<int:memberid>')
def edit(memberid):
    connection = getCursor()
    memberid = memberid 
    connection.execute("SELECT * FROM members WHERE member_id = %s;", (memberid,))
    member = connection.fetchone()
    return render_template("edit.html", member=member)

@admin_bp.route("/editmember", methods=["POST"])
def editmember():
    connection = getCursor()
    member_id=request.form.get('memberid')
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    dob = request.form.get('dob')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    subs =  request.form.get('ss')
    health_condition = request.form.get('health_condition')
    
    sql= "UPDATE members SET member_id=%s, first_name=%s, last_name=%s, dob=%s,address= %s, email= %s, phone= %s, subscription_status= %s, health_condition= %s WHERE member_id= %s;"
    connection.execute(sql,(member_id,first_name, last_name,dob, address, email,phone, subs, health_condition,member_id,))
    connection.execute("SELECT * FROM members WHERE member_id = %s;",(member_id,))
    member=connection.fetchall()
    column_names = [desc[0] for desc in connection.description]
    message = 'Member with ID {} updated successfully'.format(member_id)

    return render_template("editmember.html", member=member,column_names=column_names, message=message)

##########↓↓↓↓↓Special↓↓↓↓↓##########
@admin_bp.route('/viewclasses', methods=['GET','POST'])
def viewclasses():
    cur = getCursor()
    if request.method == 'POST':
        trainerId = request.form.get('selectTrainer', type = int)
        className = request.form.get('searchClass')
        month = request.form.get('byMonth', type = int)
        if trainerId != 0 and className == "" and month == 0:#show search result for specific trainer without class name
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE class.trainer_id = %s \
                ORDER BY Date, Start;"
            cur.execute(sql, (trainerId,))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, selectTrainer=trainerId, monthDropdownMenu=months)
        elif trainerId != 0 and className != "" and month == 0:#show search result for specific trainer plus class name
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE class.trainer_id = %s AND class.class_name LIKE '%' %s '%' \
                ORDER BY Date, Start;"
            cur.execute(sql, (trainerId,className))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, selectTrainer=trainerId, searchClass=className, monthDropdownMenu=months)
        elif trainerId == 0 and className != "" and month == 0:#show search result for all trainers plus class name    
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE class.class_name LIKE '%' %s '%' \
                ORDER BY Date, Start;"
            cur.execute(sql, (className,))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, selectTrainer=trainerId, searchClass=className, monthDropdownMenu=months)
        elif trainerId == 0 and className == "" and month == 0:#show search result for all trainers without class name
            select_result = getTrainersClasses()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, monthDropdownMenu=months)
        elif trainerId == 0 and className == "" and month != 0:#show search result for all trainers without class name in selected month
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE Month(class.class_date) = %s \
                ORDER BY Date, Start;"
            cur.execute(sql, (month,))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, byMonth=str(month), monthDropdownMenu=months)
        elif trainerId == 0 and className != "" and month != 0:#show search result for all trainers with class name in selected month
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE Month(class.class_date) = %s AND class.class_name LIKE '%' %s '%' \
                ORDER BY Date, Start;"
            cur.execute(sql, (month, className))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, searchClass=className, byMonth=str(month), monthDropdownMenu=months)
        elif trainerId != 0 and className != "" and month != 0:#show search result for specific trainer with class name in selected month
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE class.trainer_id = %s AND Month(class.class_date) = %s AND class.class_name LIKE '%' %s '%' \
                ORDER BY Date, Start;"
            cur.execute(sql, (trainerId, month, className))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, searchClass=className, byMonth=str(month), monthDropdownMenu=months, selectTrainer=trainerId)
        elif trainerId != 0 and className == "" and month != 0:#show search result for specific trainer with all their classes in selected month
            sql = "SELECT class_name AS Class, CONCAT(first_name, ' ', last_name) AS Trainer, class_date AS Date, start_time AS Start, end_time AS End \
                FROM class_schedule AS class \
                JOIN trainers AS trainers ON class.trainer_id = trainers.trainer_id \
                WHERE class.trainer_id = %s AND Month(class.class_date) = %s \
                ORDER BY Date, Start;"
            cur.execute(sql, (trainerId, month))
            select_result = cur.fetchall()
            classes = getDatesToWeekday(select_result)
            column_names = [desc[0] for desc in cur.description]
            column_names.append("Day")
            trainer_result = getAllTrainers()
            months = getMonths()
            return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, byMonth=str(month), monthDropdownMenu=months, selectTrainer=trainerId)
    else:
        select_result = getTrainersClasses()
        classes = getDatesToWeekday(select_result)
        column_names = [desc[0] for desc in cur.description]
        column_names.append("Day")
        trainer_result = getAllTrainers()
        months = getMonths()
        return render_template('viewclasses.html',dbresult=classes,dbcols=column_names,trainerDropdownMenu=trainer_result, monthDropdownMenu=months)

# @admin_bp.route('/send_message', methods=['GET', 'POST'])
# def send_message():
#     if request.method == 'POST':
#         receiver_id = request.form['receiver_id']
#         message = request.form['message']
#         sender_id = session.get('user_id')
#         timestamp = datetime.now()

##########↓↓↓↓↓Special↓↓↓↓↓##########
@admin_bp.route('/substatus', methods=['GET','POST'])
def substatus():
    cur = getCursor()
    if request.method == 'POST':
        month = request.form.get('selectMonth', type = int)
        status = request.form.get('byStatus')
        if month != 0 and status == "":
            sql = "SELECT member_id AS MemberId, CONCAT(first_name, ' ', last_name) AS Name, email AS Email, subscription_status AS Status, auto_pay AS AutoPayment, \
                  sub_duedate AS MembershipDueDate FROM members \
                  WHERE MONTH(sub_duedate) = %s \
                  ORDER BY member_id;"
            cur.execute(sql, (month,))
            sub_result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            allMonths = getMonths()
            allStatus = getSubStatus()
            session['report'] = sub_result
            return render_template("substatus.html", dbresult=sub_result, dbcols=column_names, monthDropdownMenu=allMonths, statusDropdownMenu=allStatus, selectMonth=str(month))
        elif month != 0 and status != "":
            sql = "SELECT member_id AS MemberId, CONCAT(first_name, ' ', last_name) AS Name, email AS Email, subscription_status AS Status, auto_pay AS AutoPayment, \
                  sub_duedate AS MembershipDueDate FROM members \
                  WHERE MONTH(sub_duedate) = %s AND subscription_status = %s \
                  ORDER BY member_id;"
            cur.execute(sql, (month,status))
            sub_result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            allMonths = getMonths()
            allStatus = getSubStatus()
            session['report'] = sub_result
            return render_template("substatus.html", dbresult=sub_result, dbcols=column_names, monthDropdownMenu=allMonths, statusDropdownMenu=allStatus, selectMonth=str(month), byStatus=status)
        elif month == 0 and status != "":
            sql = "SELECT member_id AS MemberId, CONCAT(first_name, ' ', last_name) AS Name, email AS Email, subscription_status AS Status, auto_pay AS AutoPayment, \
                   sub_duedate AS MembershipDueDate FROM members \
                   WHERE subscription_status = %s ORDER BY member_id;"
            cur.execute(sql, (status,))
            sub_result = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            allMonths = getMonths()
            allStatus = getSubStatus()
            session['report'] = sub_result
            return render_template("substatus.html", dbresult=sub_result, dbcols=column_names, monthDropdownMenu=allMonths, statusDropdownMenu=allStatus, byStatus=status)
        elif month == 0 and status == "":
            sub_result = getSubReport()
            column_names = [desc[0] for desc in cur.description]
            allMonths = getMonths()
            allStatus = getSubStatus()
            session['report'] = sub_result
            return render_template("substatus.html", dbresult=sub_result, dbcols=column_names, monthDropdownMenu=allMonths, statusDropdownMenu=allStatus)
    else:
        sub_result = getSubReport()
        column_names = [desc[0] for desc in cur.description]
        allMonths = getMonths()
        allStatus = getSubStatus()
        session['report'] = sub_result
        return render_template("substatus.html", dbresult=sub_result, dbcols=column_names, monthDropdownMenu=allMonths, statusDropdownMenu=allStatus)    

##########↓↓↓↓↓Special↓↓↓↓↓##########
@admin_bp.route('/substatus/export')
def subStatusExport():
    report = session.get('report')
    for i, item in enumerate(report):
        date_str = item[-1]  # Get the datetime string
        date_obj = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')  # Convert to datetime object
        report[i] = item[:-1] + (date_obj.date(),)
    cur = getCursor()
    sql = "SELECT members.member_id AS MemberId, CONCAT(first_name, ' ', last_name) AS Name, email AS Email, subscription_status AS Status, auto_pay AS AutoPayment, \
          sub_duedate AS MembershipDueDate FROM members \
          JOIN payment_detail ON members.member_id = payment_detail.member_id \
          GROUP BY members.member_id"
    cur.execute(sql)
    sub_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
#change sql result into csv file
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(column_names)
#for loop to get sql result in order
    for row in report:
        writer.writerow(row)
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-disposition': 'attachment; filename=subscriptions_Status_Report.csv'})
    
# In admin.py Na reminder
@admin_bp.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        receiver_id = request.form['receiver_id']
        message = request.form['message']
        sender_id = session.get('user_id')
        timestamp = datetime.now()

        
#         cursor = getCursor()
#         query = "INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (sender_id, receiver_id, message, timestamp))
        
#         flash('Message sent successfully!')
#         return redirect(url_for('admin.index'))
    

#     # Generate the list of members to select from
#     cursor = getCursor()
#     query = "SELECT id, username FROM members"
#     cursor.execute(query)
#     members = cursor.fetchall()
    
#     return render_template("send_message.html", members=members)

    # Generate the list of members to select from
    cursor = getCursor()
    query = "SELECT id, username FROM members"
    cursor.execute(query)
    members = cursor.fetchall()
    return render_template("send_message.html", members=members)


#####view the popular class list--Bree
@admin_bp.route("/popular_class")
def popular_class():
    connection = getCursor()
    start_date = request.args.get('start_date', default='2023-03-01')
    end_date = request.args.get('end_date', default='2023-04-30')
    if not start_date or not end_date:
        return render_template("popular_class.html", message="Please select a period to see the result")

    sql = """SELECT 
                class_schedule.class_name,
                CONCAT(trainers.first_name, ' ', trainers.last_name) AS trainername,
                COUNT(booking.bookin_id) AS number_of_booking,
                COUNT(attendance.attendance_id) AS number_of_attendance
            FROM 
                class_schedule 
                LEFT JOIN booking ON class_schedule.schedule_id = booking.class_id 
                LEFT JOIN trainers ON class_schedule.trainer_id = trainers.trainer_id
                LEFT JOIN attendance ON attendance.class_booking_id = booking.bookin_id
            WHERE 
                class_schedule.class_date BETWEEN %s AND %s
            GROUP BY 
                class_schedule.class_name, trainername
            ORDER BY 
                number_of_booking DESC;"""

    connection.execute(sql, (start_date, end_date))
    Pclass_list = connection.fetchall()
    if len(Pclass_list) == 0:
        return render_template("popular_class.html", message="There's no class booked in this period")
    return render_template("popular_class.html", Pclass_list=Pclass_list)

##########↓↓↓↓↓Special↓↓↓↓↓##########
@admin_bp.route('/financial', methods=['GET'])
def financial():
    cur = getCursor()
    subRevenue = "SELECT MONTH(payment_date) AS Month, SUM(payment_amount) AS Sub_profit FROM payment_detail WHERE MONTH(payment_date) = %s GROUP BY Month"
    subRevenue_result = []
    for tuple in getMonths():
        month = tuple[0]
        cur.execute(subRevenue, (month,))
        result = cur.fetchone()
        if result == None:
            result = (month , ('0.00')) 
        subRevenue_result.append(result)
    ptRevenue = "SELECT MONTH(pt_class_payment_date) AS PTMonth, SUM(pt_class_payment_amount) AS pt_profit FROM pt_class_payment WHERE MONTH(pt_class_payment_date) = %s GROUP BY PTMonth"
    ptRevenue_result = []
    for tuple in getMonths():
        month = tuple[0]
        cur.execute(ptRevenue, (month,))
        result = cur.fetchone()
        if result == None:
            result = (month , ('0.00'))  
        ptRevenue_result.append(result)
    totalRevenue = "SELECT IFNULL(Month,0) AS Mounth, IFNULL(SUM(Profit),0) AS Total FROM \
                    (SELECT MONTH(cp.payment_date) AS Month, SUM(cp.payment_amount) AS Profit FROM payment_detail cp \
                    WHERE MONTH(cp.payment_date) = %s \
                    UNION \
                    SELECT MONTH(pt.pt_class_payment_date) AS PTMonth, SUM(pt.pt_class_payment_amount) AS pt_profit FROM pt_class_payment pt \
                    WHERE MONTH(pt.pt_class_payment_date) = %s) t GROUP BY Month"
    totalRevenue_result = []
    for tuple in getMonths():
        month = tuple[0]
        cur.execute(totalRevenue, (month, month))
        result = cur.fetchall()
        totalRevenue_result.append(result)
    allMonths = [("JAN",),("FEB",),("MAR",),("APR",),("MAY",),("JUN",),("JUL",),("AUG",),("SEP",),("OCT",),("NOV",),("DEC",)]
    return render_template("financial.html", monthsCols = allMonths, subRevenue = subRevenue_result, ptRevenue = ptRevenue_result, totalRevenue = totalRevenue_result)

### 32# attendance report Frank
@admin_bp.route('/attendance_summary', methods=['GET'])
def attendance_summary():
    # Get parameters from query string
    connection= getCursor()
    start_date = request.args.get('start_date', datetime.datetime.now().strftime('%Y-%m-%d')) # Default to today
    end_date = request.args.get('end_date', datetime.datetime.now().strftime('%Y-%m-%d')) # Default to today
    
    # Query the database for attendance data
    connection.execute("SELECT member_id, attendance_date, attendance_type FROM attendance WHERE attendance_date BETWEEN %s AND %s", (start_date, end_date))
    rows = connection.fetchall()
    member_id =''
    attendance_date = ''
    attendance_type = ''
    attendance_type_text = ''
    # Calculate summary data
    summary_data = {'total_count': 0, 'daily_count': {}, 'type_count': {'group_class': 0, 'personal_training_session': 0, 'use_gym_only': 0}}
    for row in rows:
        member_id = row[0]
        attendance_date = row[1].strftime('%Y-%m-%d')
        attendance_type = row[2]
        
        # Add to daily count
        if attendance_date not in summary_data['daily_count']:
            summary_data['daily_count'][attendance_date] = {'total': 0, 'group_class': 0, 'personal_training_session': 0, 'use_gym_only': 0}
            summary_data['daily_count'][attendance_date]['total'] += 1
        if attendance_type == 1:
            summary_data['daily_count'][attendance_date]['group_class'] += 1
            summary_data['type_count']['group_class'] += 1
            attendance_type_text = 'group class'
        elif attendance_type == 2:
            summary_data['daily_count'][attendance_date]['personal_training_session'] += 1
            summary_data['type_count']['personal_training_session'] += 1
            attendance_type_text = 'personal training session'
        elif attendance_type == 3:
            summary_data['daily_count'][attendance_date]['use_gym_only'] += 1
            summary_data['type_count']['use_gym_only'] += 1
            attendance_type_text = 'use the gym only'
        
        # Add to total count
        summary_data['total_count'] += 1
    
    # Render the HTML template with the summary data
    return render_template('attendance_summary.html', member_id =member_id, start_date=start_date, end_date=end_date, summary_data=summary_data,rows=rows,attendance_type_text=attendance_type_text,)