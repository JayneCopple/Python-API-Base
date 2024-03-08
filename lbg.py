"""
LBG learning-oriented CRUD-based RESTful API using standard Flask routing
"""

# import Flask microframework and associated tools
from flask import Flask, request, jsonify
from flask_api import status

# import SQL Alchemy (including ORM - Object-relational Mapper - and its data mapper pattern)
from models import db, ItemModel
from sqlalchemy import exc
import os

# JavaScript/ES6 text/plain MIME Content type fix (avoids registry hack!)
import mimetypes
mimetypes.add_type('text/javascript', '.js')

# set up the app with listening socket for http requests and appropriate hostname

# get app to serve static files from the public directory
app = Flask(__name__, static_url_path=f'/', static_folder='./static')

# set up a new database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# global variable for id (module private; also avoids standard library function reference collision)
_id = 1


def item_builder(item_name: str, item_description: str, item_price: float, item_id: int) -> dict:
    """
    Function to build an item
    takes in a name, description, price, and id
    uses standard library dictionary to create an item object
    """
    item: dict[str | int | float] = {
        "name": item_name,
        "description": item_description,
        "price": item_price,
        "_id": item_id,
    }
    # returns that item object
    return item


@app.before_first_request
def create_table():
    """
    Create table - only if it doesn't already exist.
    Note. If API non-persistence required, data DB will need to be reset (API controls id statelessly)
    i.e. no db look up for max id value for restart.  A possible enhancement.
    """
    db.create_all()


@app.route('/create', methods=['POST'])
def create():
    """
    CREATE (Post)
    """
    global _id

    # log that we are running the create operation
    print('Create - POST')

    # create an item from the Posted request's body data
    posted_data = request.get_json()
    name = posted_data['name']
    description = posted_data['description']
    price = posted_data['price']
    item = item_builder(name, description, float(price), int(_id))

    # insert the item into our Database
    item = ItemModel(**item)
    db.session.add(item)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as err:
        # if there is an error, send back the error
        return jsonify(str(err))

    # increment our id
    _id += 1

    # otherwise 201 - Created and the item
    json_item = jsonify(str(item.serialize))

    # log that item to console
    print(f'Created item: {json_item}')

    return json_item, status.HTTP_201_CREATED


@app.route('/read', methods=['GET'])
def read_all():
    """
    READ ALL (Get)
    """
    # log that we are running the read operation
    print('Read - GET')

    # reading all items from database

    items = ItemModel.query.all()
    if not items:
        # if there is an error, send back the error
        return jsonify(items), status.HTTP_200_OK
    else:
        # otherwise 200 - OK
        serialized_items = [item.serialize for item in items]
        json_items = jsonify(serialized_items)

        # log the items to console
        print(f'Reading items: {serialized_items}')

        return json_items, status.HTTP_200_OK


@app.route('/read/<int:_id>', methods=['GET'])
def read_one(_id):
    """
    READ ONE (Get)
    """
    # log that we are running the read operation
    print('\nRead items - GET\n')

    # reading item from database by id
    item = ItemModel.query.filter_by(_id=int(_id)).first()

    if not item:
        # if there is an error, send back empty list (standardised API design choice)
        print(f'Reading item: []')
        return jsonify([]), status.HTTP_200_OK

    # otherwise 200 - OK
    print(f'Reading item: {item.serialize}')
    json_item = jsonify(item.serialize)
    return json_item, status.HTTP_200_OK


@app.route('/update/<int:_id>', methods=['PUT'])
def update_one(_id):
    """
    UPDATE (Put)
    """
    # log that we are running the read operation
    print('Update - PUT')

    # create an item from the Posted request's body data
    posted_data = request.get_json()
    name = posted_data['name']
    description = posted_data['description']
    price = posted_data['price']
    updated_item = item_builder(name, description, price, int(_id))

    # find data in database BY using the id
    item = ItemModel.query.filter_by(_id=int(_id)).first()

    if not item:
        # if there is an error, send back the error (0 to match previous API implementation)
        print(f'Updated item id: 0')
    else:
        # send the new item
        db.session.query(ItemModel).filter(ItemModel._id == item._id).update(updated_item, synchronize_session=False)
        db.session.commit()

        # log the item ID being returned
        print(f'Updated item id: {_id}')

    # otherwise 200 - OK
    return "OK", status.HTTP_200_OK


@app.route('/delete/<int:_id>', methods=['DELETE'])
def delete_one(_id):
    """
    DELETE (Delete)
    """
    # log that we are running the delete operation
    print('Delete - DELETE')

    # find data in database BY using the id
    item = ItemModel.query.filter_by(_id=int(_id)).first()

    try:
        # deleting item from database by id
        db.session.delete(item)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        # if there is an error, send back the error (0 to match previous API implementation)
        print(f'Deleted item id: 0')

    else:
        # log the item ID being returned
        print(f'Deleted item id: {_id}')

    # otherwise 200 - OK
    return "OK", status.HTTP_200_OK


# module import protection
if __name__ == '__main__':
    # get app to serve
    PORT = (os.getenv('PORT', 80))
    HOST = '0.0.0.0'
    print(f'API Listening on http://{HOST}:{PORT}')
    app.run(host=HOST, port=PORT, debug=True)
