from flask import Blueprint, render_template, request, json, url_for
from werkzeug.utils import redirect
from src.models.stores.store import Store
import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id))


@store_blueprint.route('/edit/<string:store_id>', methods=['GET','POST'])
@user_decorators.requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method=='POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.price_tag = request.form['price_tag']
        store.price_query = request.form['price_query']
        store.img_query = request.form['img_query']
        store.img_src_tag = request.form['img_src_tag']
        store.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET','POST'])
@user_decorators.requires_admin
def create_store():
    if request.method=='POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        price_tag = request.form['price_tag']
        price_query = json.loads(request.form['price_query'])
        img_query = json.loads(request.form['img_query'])
        img_src_tag = request.form['img_src_tag']
        Store(name, url_prefix, price_tag, price_query, img_query, img_src_tag).save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('stores/new_store.html')