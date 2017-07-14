from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# make sure we can access the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def getRestaurants():
    restaurantList = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurantList)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def addRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('getRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('getRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=editRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    remove_this_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(remove_this_restaurant)
        session.commit()
        return redirect(url_for('getRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=remove_this_restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def getRestaurantMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['name'], price=request.form['price'], description=request.form['descr'], restaurant=restaurant)
        session.add(newMenuItem)
        session.commit()
        return redirect(url_for('getRestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        editedItem.name = request.form['name']
        editedItem.price = request.form['price']
        editedItem.description = request.form['descr']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('getRestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    remove_this_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        session.delete(remove_this_item)
        session.commit()
        return redirect(url_for('getRestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=remove_this_item)



if __name__ == '__main__':
    app.debug = True # restart server on changes
    app.run(host = '0.0.0.0', port = 5000)
