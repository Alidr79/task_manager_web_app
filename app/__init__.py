from flask import Flask, session
from config import config  # --> the second config is the dict that we have defined
from flask_login import LoginManager
import datetime

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Please login to your account'


def time_to(deadline, diff):
    _delay_string = None
    if diff == "Nothing":
        _delay_string = "An error happened"
        return _delay_string

    input_time = datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    delta = (input_time - now).total_seconds()
    # Add the difference of dateTime between server and user
    delta += diff

    delta_minute = int(delta / 60)
    delta_hour = int(delta / (60 * 60))
    delta_day = int(delta / (60 * 60 * 24))

    if delta < 0:
        _delay_string = "Overdue"

    elif delta < 60:
        _delay_string = "less than a minute remaining"

    elif delta_minute < 60:
        if delta_minute == 1:
            _delay_string = "1 minute remaining"
        else:
            _delay_string = "{} minutes remaining".format(delta_minute)

    elif delta_hour < 24:
        if delta_hour == 1:
            _delay_string = "1 hour remaining"
        else:
            _delay_string = "{} hours remaining".format(delta_hour)

    elif delta_day < 50:
        if delta_day == 1:
            _delay_string = "1 day remaining"
        else:
            _delay_string = "{} days remaining".format(delta_day)
    else:
        _delay_string = "long time remaining"

    return _delay_string


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)

    # custom functions
    app.jinja_env.globals.update(time_to=time_to)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
