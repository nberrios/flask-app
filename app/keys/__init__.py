from flask import Blueprint


bp = Blueprint('keys', __name__, template_folder='templates')


from app.keys import routes
