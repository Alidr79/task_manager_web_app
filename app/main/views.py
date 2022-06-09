import datetime

from flask import flash
from flask import render_template, redirect, url_for
from flask import request, session
from flask_login import login_required, login_user, logout_user, current_user

from . import main
from ..db_work import database
from ..user import load_user

EMOJIE_PURE_LIST = ["#128640", "#128170", "#128163", "#128218", "#128181", "#9989", "#9940", "#9888", "#8987",
                    "#9760", "#10002", "#128705", "#128680", "#128679", "#128564",
                    "#128556", "#128557", "#128548", "#128515"]


@main.route('/')
@login_required
def index():
    user_id = current_user.get_id()
    task_list = database().get_all_user_tasks(user_id)
    connection = database().get_connection()
    result = connection.execute("SELECT diff FROM user WHERE user_id = ?",
                       [user_id]).fetchone()
    connection.close()
    if result is not None:
        return render_template('index.html', task_list=task_list, diff=result['diff'])
    else:
        return render_template('index.html', task_list=task_list, diff="Nothing")


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        ticket_number = request.form.get('ticket_number')
        user_password = request.form.get('user_password')
        user_dateTime = request.form.get('current_dateTime')
        user_dateTime = user_dateTime.replace('T', ' ') + ':00'

        is_valid = database().check_password(ticket_number, user_password)
        if is_valid:
            user_obj = load_user(ticket_number)
            login_user(user_obj, remember=True)

            # diff_dateTime is the difference between server and user
            user_dateTime = datetime.datetime.strptime(user_dateTime, '%Y-%m-%d %H:%M:%S')
            server_dateTime = datetime.datetime.now()
            diff = (server_dateTime - user_dateTime).total_seconds()
            connection = database().get_connection()
            connection.execute("UPDATE user SET diff = ? WHERE user_id = ?",
                               (diff, ticket_number))
            connection.commit()
            connection.close()

            return redirect(url_for('main.index'))
        else:
            flash('Incorrect ticket or password')
            return redirect(url_for('main.login'))

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('main.index'))


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        ticket_number = request.form.get('ticket_number')
        invite_code = request.form.get('invite_code')
        user_password = request.form.get('user_password')
        user_dateTime = request.form.get('current_dateTime')

        status = database().check_new_user(ticket_number, invite_code)
        if status == -2:
            flash("Not found!")
            return redirect(url_for('main.signup'))

        elif status == 1:
            successful_add = database().add_new_user(ticket_number, user_password, user_dateTime)
            if successful_add:
                flash("User was successfully added")
                user_obj = load_user(ticket_number)
                login_user(user_obj, remember=True)
                return redirect(url_for('main.index'))

        elif status == 0:
            flash("This invite code is expired")
            return redirect(url_for('main.signup'))

        elif status == -1:
            flash("Invalid invite_code")
            return redirect(url_for('main.signup'))
    return render_template('signup.html')


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == "POST":
        task_name = request.form['task_name']
        task_desc = request.form['task_desc']
        task_emoji = request.form['task_emoji']
        task_color = int(request.form['task_color'])
        deadline_isactive = request.form.getlist('deadline_isactive')
        task_deadline = request.form['task_deadline']

        if len(task_name) > 25 or len(task_desc) > 50:
            flash("Error in adding the task")
            return redirect(url_for('main.add_task'))

        add_status = False
        is_active = 0
        if 'on' in deadline_isactive:
            is_active = 1
            print("$ on" * 20)
            task_deadline = task_deadline.replace('T', ' ') + ':00'
            deadline_time = datetime.datetime.strptime(task_deadline, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            if (deadline_time - now).total_seconds() < 0:
                flash("Task deadline couldn't be before the the current time!")
                return redirect(url_for('main.add_task'))

        add_status = database().add_task(task_name, task_desc, task_emoji, task_color, is_active,
                                         task_deadline, current_user.get_id())
        if add_status:
            flash("Task added to the board")
            return redirect(url_for('main.index'))
        else:
            flash("Error in task add")
            return redirect(url_for('main.add_task'))

    return render_template('add.html', emojis_pure=EMOJIE_PURE_LIST)


@main.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    if database().check_author(current_user.get_id(), task_id):
        if database().delete_task(task_id):
            flash("Task deleted")
        else:
            flash("Sorry an error happened")
    else:
        flash("Access denied!")

    return redirect(url_for('main.index'))
