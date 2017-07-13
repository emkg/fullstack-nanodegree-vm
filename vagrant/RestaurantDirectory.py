from flask import Flask, render_template, url_for, request, redirect, jsonify
app = Flask(__name__)

# import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# make sure we can access the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def getRestaurants():
    return render_template('restaurants.html', restaurant=Restaurant)

@app.route('/restaurant/new')
def addRestaurant():
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return render_template('editRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return render_template('deleteRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def getRestaurantMenu(restaurant_id):
    return render_template('menu.html', restaurant=Restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def addMenuItem(restaurant_id):
    return render_template('newMenuItem.html')

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editMenuItem.html')

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html')



if __name__ == '__main__':
    app.debug = True # restart server on changes
    app.run(host = '0.0.0.0', port = 5000)
