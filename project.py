from flask import Flask
from flask import render_template
from flask import request, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, CatalogItem, Base, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Catalog Items'


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Create anti-forgery state token

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state

    # return "The current session state is %s" % login_session['state']

    return render_template('login.html', STATE=state, log=login_session)


@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps('Failed to upgrade authorization code.'
                                     ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps(
                "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps(
                            "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<center><h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += \
        '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    output += ' <div class="alert alert-success">'
    output += 'You are redericted through your gmail account:<strong>'
    output += login_session['email']
    output += '</strong>......</div></center>'
    flash('you are now logged in as %s' % login_session['username'])
    return output


# Disconnect - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect', methods=['GET', 'POST'])
def gdisconnect():

    # Only disconnect a connected user.

    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

        # Execute HTTP GET request to revoke current token

    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':

        # Reset the user's session

        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('User disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = \
            make_response(json.dumps('''Failed to revoke token for \
                                given user!
result = %s
 credentials = %s \
                                '''
                          % (result, credentials)), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Connect to Databse and create database session
engine = create_engine('sqlite:///catalogitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


# Show all Catalog and Latest Items

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    """Show the catalog"""

    catalog = session.query(Catalog).order_by(asc(Catalog.name))
    latestItems = \
        session.query(CatalogItem).order_by(desc(CatalogItem.id)).limit(6)
    return render_template('catalog.html', catalog=catalog,
                           items=latestItems)


@app.route('/catalog/<string:name>/items/')
def showItems(name):
    """ Show Items ordered by directory """

    catalog = session.query(Catalog).order_by(asc(Catalog.name))
    catalogParticular = \
        session.query(Catalog).filter_by(name=name).one()
    items = \
        session.query(CatalogItem).filter_by(catalog_id=catalogParticular.id).all()  # NOQA
    count = \
        session.query(CatalogItem).filter_by(catalog_id=catalogParticular.id).count()  # NOQA
    return render_template('catalogitems.html', catalog=catalog,
                           catalogParticular=catalogParticular,
                           count=count, items=items)


@app.route('/catalog/<string:name>/<string:itemName>/')
def showParticularItem(name, itemName):
    """Description of Particular Item of Catalog"""

    item = session.query(CatalogItem).filter_by(title=itemName,
                                                category=name).one()

    if 'username' not in login_session:
        return render_template('publicitemdescription.html', item=item)
    else:
        return render_template('itemdescription.html', item=item)


@app.route('/catalog/newItem', methods=['GET', 'POST'])
@login_required
def addItem():
    """Adding an item to database"""

    catalog = session.query(Catalog)
    user = getUserbyEmail(login_session['email'])
    if request.method == 'POST':

        # Checking if data is correct

        if request.form['title'] == '' or request.form['description'] == '':
            return render_template('newitem.html', catalog=catalog,
                                   error='Please Enter Data in the fields!'
                                   )

        # Checking if there is item which already exist in particular category

        if session.query(CatalogItem).filter_by(title=request.form['title'], category=request.form['catalog_item']).count() != 0:  # NOQA
            return render_template('newitem.html', catalog=catalog,
                                   error='Item Already Exist in given Category'
                                   )

        catalogParticular = \
            session.query(Catalog).filter_by(
                name=request.form['catalog_item']).one()
        newItem = CatalogItem(title=request.form['title'],
                              description=request.form['description'],
                              category=request.form['catalog_item'],
                              catalog=catalogParticular, user=user)
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % newItem.title)
        return redirect(url_for('showItems',
                        name=catalogParticular.name))
    else:
        return render_template('newitem.html', catalog=catalog, error=''
                               )


@app.route('/catalog/<string:name>/<string:itemName>/edit/',
           methods=['GET', 'POST'])
@login_required
def editItem(name, itemName):
    """ Editing a particular item """

    catalog = session.query(Catalog)
    catalogParticular = \
        session.query(CatalogItem).filter_by(title=itemName,
                                             category=name).one()
    if catalogParticular.user_id != login_session['user_id']:
        flash('You are not authorised to edit %s' % catalogParticular.title
              )
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':

        # Checking if there is a valid data or not

        if request.form['title'] == '' or request.form['description'] == '':
            return render_template('edititem.html', catalog=catalog,
                                   error='Please Enter Data in the fields!',
                                   catalogParticular=catalogParticular)

        # Checking if there is an item which already exists
        # in particular category

        if session.query(CatalogItem).filter_by(title=request.form['title'], category=request.form['catalog_item']).count() != 0:  # NOQA
            return render_template(
                'edititem.html', catalog=catalog,
                error='Item Already Exists in given Category',
                catalogParticular=catalogParticular)

        if request.form['title']:
            catalogParticular.title = request.form['title']
        if request.form['description']:
            catalogParticular.description = request.form['description']
        if request.form['catalog_item']:
            catalogParticular.category = request.form['catalog_item']
        catalogParticular.catalog = \
            session.query(Catalog).filter_by(name=request.form['catalog_item']).one()  # NOQA
        session.add(catalogParticular)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItems',
                        name=catalogParticular.category))
    else:
        return render_template('edititem.html', catalog=catalog,
                               error='',
                               catalogParticular=catalogParticular)


@app.route('/catalog/<string:name>/<string:itemName>/delete/',
           methods=['GET', 'POST'])
@login_required
def deleteItem(name, itemName):
    """ Deleting a particular item """

    catalogParticular = \
        session.query(CatalogItem).filter_by(title=itemName,
                                             category=name).one()

    if catalogParticular.user_id != login_session['user_id']:
        flash('You are not authorised to delete %s' % catalogParticular.title
              )
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        session.delete(catalogParticular)
        session.commit()
        flash('Item  %s Successfully deleted' % catalogParticular.title)
        return redirect(url_for('showItems',
                        name=catalogParticular.category))
    else:
        return render_template('deleteitem.html',
                               catalogParticular=catalogParticular)


# JSON APIs to view All Catalog Information

@app.route('/catalog/JSON')
def CatalogJSON():
    """JSONifying catalog"""

    items = session.query(CatalogItem).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


# JSON APIs to view particular Catalog Information

@app.route('/catalog/<string:itemName>/JSON')
def CatalogParticularItemJSON(itemName):
    """JSONifying Particular Item """

    items = \
        session.query(CatalogItem).filter_by(category=itemName).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/catalog/User/JSON')
def CatalogItemJSON():
    """ JSONifying particular item"""

    items = session.query(User)
    return jsonify(CatalogItems=[i.serialize for i in items])


def getUserID(email):
    """ Getting particular User id using his/her email"""

    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserbyEmail(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user
    except:
        return None


def getUserInfo(user_id):
    """ Getting User using user id"""

    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    """ Creating User using login session """

    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
