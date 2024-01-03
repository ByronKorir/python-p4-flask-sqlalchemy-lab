#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal =  Animal.query.filter(Animal.id == id).first()

    if not animal:
        respose_body = '<h1>No Animal Found</h1>'
        response = make_response(respose_body,404)
        return response
        

    respose_body = f''
    respose_body += f'<ul>ID: {animal.id}</ul>'
    respose_body += f'<ul>Name; {animal.name}</ul>'
    respose_body += f'<ul>Species: {animal.species}</ul>'
    respose_body += f'<ul>Zookeeper: {animal.zookeeper.name}</ul>'
    respose_body += f'<ul>Enclosure Environment: {animal.enclosure.environment}</ul>'
    
    response = make_response(respose_body,200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zk = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zk:
        response_body = '<h1>No Zookeeper found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f''
    response_body += f'<ul>ID: {zk.id}</ul>'
    response_body += f'<ul>Name: {zk.name}</ul>'
    response_body += f'<ul>Birthday: {zk.birthday}</ul>'

    animals = [animal for animal in zk.animals]
    for animal in animals:
        response_body += f'<ul>Animal=> {animal.name} ||   Species => {animal.species}</ul>'
        if not animal:
            response_body += f'<ul>Not assigned an animal yet</ul>'
    
    response = make_response(response_body,200)

    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    en = Enclosure.query.filter(Enclosure.id == id).first()

    if not en:
        response_body = '<h1>No environment Found</h1>'
        return make_response(response_body,404)

    response_body = f''
    response_body += f'<ul>ID: {en.id}</ul>'
    response_body += f'<ul>Environment: {en.environment}</ul>'
    response_body += f'<ul>Open ?: {en.open_to_visitors}</ul>'

    animals = [animal for animal in en.animals]
    for animal in animals:
        response_body += f'<ul>Animal=> {animal.name} ||   Species => {animal.species}</ul>'
        if not animal:
            response_body += f'<ul>Has no animal yet</ul>'

    response = make_response(response_body,20)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
