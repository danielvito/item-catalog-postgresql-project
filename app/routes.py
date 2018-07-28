#!/usr/bin/env python

from app import app
from app import babel
from app import db
from app.models import Brand, Category, CategoryItem, User, \
    CategorySchema, CategoryItemSchema
from app.categoryitemform import CategoryItemForm
from app.util import Util
from config import Config
from flask import render_template, jsonify, session as login_session, \
    make_response, request, flash, redirect, url_for
from flask_babel import _
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
import requests

CLIENT_ID = json.loads(
    open(Config.CLIENT_SECRET_JSON, 'r').read())['web']['client_id']


@babel.localeselector
def get_locale():
    if 'language' not in login_session:
        login_session['language'] = 'en'
    return login_session['language']


@app.context_processor
def inject_language():
    LANG_NAMES = {'en': _('english'), 'pt_br': _('portuguese')}
    return dict(languages=LANG_NAMES, cur_lang=login_session['language'])


@app.route('/language/<string:language>')
def set_site_language(language):
    login_session['language'] = language
    return redirect(url_for('show_categories'))


def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            flash(_("please_login"))
            return redirect(url_for('show_login'))
        return function_to_protect(*args, **kwargs)
    return wrapper


@app.route('/')
@app.route('/index')
@app.route('/index/')
@app.route('/catalog')
@app.route('/catalog/')
@app.route('/catalog/<int:category_id>/items', methods=['GET', 'POST'])
def show_categories(category_id=None):
    categories = Category.list_categories()
    items = CategoryItem.list_category_items_by_category(category_id)

    cat_count = {}
    for category in categories:
        cat_count[category.id] = CategoryItem.count_by_category(category.id)

    return render_template('categories.html', categories=categories,
                           items=items, cat_count=cat_count,
                           selected_category_id=category_id)


@app.route('/catalog/item/<int:categoryitem_id>', methods=['GET', 'POST'])
def show_categoryitem_read(categoryitem_id=None):
    return manage_categoryitem(categoryitem_id=categoryitem_id, type_op=1)


@app.route('/catalog/new/', methods=['GET', 'POST'])
@login_required
def show_categoryitem_new():
    return manage_categoryitem(categoryitem_id=None, type_op=2)


@app.route('/catalog/update/<int:categoryitem_id>', methods=['GET', 'POST'])
@login_required
def show_categoryitem_update(categoryitem_id=None):
    return manage_categoryitem(categoryitem_id=categoryitem_id, type_op=3)


@app.route('/catalog/delete/<int:categoryitem_id>', methods=['GET', 'POST'])
@login_required
def show_categoryitem_delete(categoryitem_id=None):
    return manage_categoryitem(categoryitem_id=categoryitem_id, type_op=4)


def manage_categoryitem(categoryitem_id=None, type_op=1):
    """
    Manage category item CRUD

    Args:
        param1: category item id
        param2: operation type (1 -> read, 2 -> new, 3 -> update, 4 -> delete)
    """
    item = CategoryItem.by_id(categoryitem_id)

    if item is None and type_op != 2:
        flash(_('no_found_rows'))

    if type_op == 4:
        db.session.delete(item)
        db.session.commit()
        flash(_('item_deleted_successfully'))
        return redirect(url_for('show_categories'))

    form = CategoryItemForm(request.form)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    form.brand_id.choices = [(b.id, b.name) for b in Brand.query.all()]

    if item is not None and request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.price.data = item.price
        form.category_id.data = item.category_id
        form.brand_id.data = item.brand_id

    if request.method == 'POST' and form.validate():
        if categoryitem_id is not None:
            item.name = form.name.data
            item.description = form.description.data
            item.price = form.price.data
            item.category = Category.get_by_id(id=form.category_id.data)
            item.brand = Brand.get_by_id(id=form.brand_id.data)
            item.user = User.get_by_id(login_session['user_id'])
            flash(_('item_updated_successfully'))
        else:
            item = CategoryItem(name=form.name.data,
                                description=form.description.data,
                                price=form.price.data,
                                category=Category.get_by_id(id=form.category_id.data),  # noqa
                                brand=Brand.get_by_id(id=form.brand_id.data),  # noqa
                                user=User.get_by_id(login_session['user_id']))  # noqa
            flash(_('item_added_successfully'))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('show_categoryitem_read', categoryitem_id=item.id))  # noqa

    return render_template('categoryitem.html', item=item, type_op=type_op,
                           form=form)


@app.route('/catalog/JSON')
def catagoryItemsJSON():
    categories_schema = CategorySchema(many=True)
    categories = Category.query.all()
    result = categories_schema.dump(categories)
    return jsonify({'categories': result})


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/login_successful')
def show_login_successful():
    return render_template("login_successful.html")


@app.route('/failed_server_side_call')
def show_login_error():
    return render_template("login_error.html")


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        return Util.custom_make_response(json.dumps(_('invalid_state_parameter')), 401)  # noqa
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(Config.CLIENT_SECRET_JSON,
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return Util.custom_make_response(json.dumps(_('failed_to_upgrade_the_authorization_code')), 401)  # noqa

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return Util.custom_make_response(json.dumps(result.get('error')), 500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return Util.custom_make_response(json.dumps(_("tokens_user_id_doesnt_match_given_user_id")), 401)  # noqa

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return Util.custom_make_response(json.dumps(_("tokens_client_id_does_not_match_apps")), 401)  # noqa

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    user = User.check_new_user(name=data['name'],
                               email=data['email'],
                               picture=data['picture'])
    if user is None or not user.id:
        return Util.custom_make_response(json.dumps(_("invalid_user")), 401)

    login_session['user_id'] = user.id
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    return '1'


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        return Util.custom_make_response(json.dumps(_('current_user_not_connected')), 401)  # noqa
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']

    del login_session['user_id']
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    h = httplib2.Http()
    result, content = h.request(url, 'GET')

    response_code = 0
    response_msg = ''
    if result['status'] == '200':
        response_code = 200
        response_msg = 'successfully_disconnected'
    else:
        response_code = 400
        response_msg = _('failed_to_revoke_token_for_given_user')

    return Util.custom_make_response(json.dumps(response_msg), response_code)
