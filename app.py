import re
from datetime import date, datetime, timedelta

import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler

from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)
from mysql.connector import FieldType
import re
from datetime import datetime, timedelta
import connect
from admin.admin import admin_bp
from member.member import member_bp
from trainer.trainer import trainer_bp

app = Flask(__name__)



# Register blueprints

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(member_bp, url_prefix='/member')
app.register_blueprint(trainer_bp, url_prefix='/trainer')

if __name__ == '__main__':
    app.run()
# for the session
app.secret_key = 'some secret key'

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginuser", methods=['GET', 'POST'])
def loginuser():
    if request.method == 'POST':
        # get username from the login
        username = request.form.get('username')
        connection = getCursor()
        connection.execute("SELECT role FROM user WHERE username=%s", (username,))
        rows = connection.fetchall()
        if len(rows) > 0:
            role = rows[0][0]
            # store username in session
            session['username'] = username
            if role== 'admin':
                return redirect(url_for('admin.index'))
            elif role == 'member':
                # update attendance table when member only use the gym
                connection.execute("SELECT member_id, subscription_status FROM members WHERE email = %s;",(username,))
                result = connection.fetchone()
                member_id = result[0]
                subscription_status = result[1]
                attendance_date = datetime.now().date()
                if subscription_status == 'active':
                    connection.execute("INSERT INTO attendance (member_id, attendance_date, attendance_type) VALUES (%s, %s, '3');", (member_id, attendance_date,))
                    connection.close()
                else:
                    connection.close()
                return redirect(url_for('member.index'))
            # username to change profile
            elif role == 'trainer':
                return redirect(url_for('trainer.index'))
        else:
            error = 'Please provide a valid username.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route("/join")
def join():
    return render_template("join.html")

@app.route("/gymschedule")
def gymschedule():
    return render_template("gymschedule.html")

 # scheduled job

# def update_subscription_status():
#     cur = getCursor()
#     todaydate = date.today()
#     todaydate_str = todaydate.strftime('%Y-%m-%d') # convert date to string
   
    

    
#     cur.execute("UPDATE members SET subscription_status ='inactive' WHERE sub_duedate=%s;",(todaydate_str,)) 



# scheduler = BackgroundScheduler(daemon=True)
# check every day midnight

# scheduler.add_job(update_subscription_status, 'cron',  minute='*', id='my_job_id', replace_existing=True)
# scheduler.start()

