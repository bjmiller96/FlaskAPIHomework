from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# Create car endpoint
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    cost = request.json['cost']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(year, make, model, cost, user_token = user_token)
    db.session.add(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Retrieve cars endpoint
@api.route('/cars', methods = ['GET'])
@token_required
def get_all_cars(current_user_token):
    a_car = current_user_token.token
    cars = Car.query.filter_by(user_token = a_car).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieve single car endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    c_owner = current_user_token.token
    if c_owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Message': 'Valid Token Required'}), 401

# Update car endpoint
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update(current_user_token, id):
    car = Car.query.get(id)
    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.cost = request.json['cost']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete car endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)