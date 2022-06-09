from flask import Blueprint

main = Blueprint('main' , __name__)
# the following line is 100% important
# if you don't write this line, the app doesn't work:
from . import views