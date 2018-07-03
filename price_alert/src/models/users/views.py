from flask import Blueprint, request, session, url_for, render_template, jsonify
from werkzeug.utils import redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['POST'])
def login_user():
    email = request.form['loginEmail']
    password = request.form['loginPassword']
    try:
        if User.is_login_valid(email, password):
            session['email']=email
            return jsonify(status='ok', url=url_for(".user_alerts"))
    except UserErrors.UserError as e:
        return jsonify(status='error', message=e.message)


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    email = request.form['registerEmail']
    password = request.form['registerPassword']
    try:
        if User.register_user(email, password):
            session['email']=email
            return jsonify(status='ok', url=url_for(".user_alerts"))
    except UserErrors.UserError as e:
        return jsonify(status='error', message=e.message)


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

