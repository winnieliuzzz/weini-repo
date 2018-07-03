from flask import Blueprint, render_template, request, session, url_for, jsonify
from werkzeug.utils import redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/new', methods=['GET','POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == "POST":
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)
        item.save_to_mongo()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() #this already saves to mongoDB
        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    price_limit = float(request.form['price_limit'])
    alert.price_limit = price_limit
    alert.save_to_mongo()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    alert = Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    alert = Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    alert = Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/check_price/<string:alert_id>')
@user_decorators.requires_login
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html', alert=alert)



