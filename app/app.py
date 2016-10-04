from flask import Flask
from flask import jsonify, request, session # import objects from the flask module
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask import Response
# initate flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:N@tasha2702@mysqlserver:3306/cmpe273'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Expenses(db.Model):
    __tablename__ = 'Expenses'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    email = db.Column('email', db.String(50))
    category = db.Column('category', db.String(50))
    description = db.Column('description', db.String(50))
    link = db.Column('link', db.String(100))
    estimated_costs = db.Column('estimated_costs', db.Integer)
    submit_date = db.Column('submit_date', db.DateTime, default=db.func.now())
    status = db.Column('status', db.String(20))
    decision_date = db.Column('decision_date', db.DateTime)



    def __init__(self, name, email, category, description, link, estimated_costs, submit_date):
        self.name = name
        self.email = email
        self.category = category
        self.description = description
        self.link = link
        self.estimated_costs = estimated_costs
        self.submit_date = submit_date
        self.status = "pending"

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'             : self.id,
           'name'           : self.name,
           'email'          : self.email,
           'category'       : self.category,
           'description'    : self.description,
           'link'           : self.link,
           'estimated_costs': self.estimated_costs,
           'submit_date'    : self.submit_date,
           'status'         : self.status,
           'decision_date'  : self.decision_date
            }

@app.route('/v1/expenses/<int:id>', methods = ['GET'])
def retrieve_record(id):
        record = Expenses.query.get(id)
        record = Expenses.query.filter_by(id=id).first()
        return jsonify(result=[record.serialize])


@app.route('/v1/expenses/', methods = ['POST'])
def post_record():
        temp_json = request.get_json(force=True)
        name = request.json['name']
        email = request.json['email']
        category = request.json['category']
        description = request.json['description']
        link = request.json['link']
        estimated_costs = request.json['estimated_costs']
        submit_date = datetime.now()
        record = Expenses(name, email, category, description, link, estimated_costs,submit_date)

        db.create_all();
        db.session.add(record)
        db.session.commit()

        record = Expenses.query.filter_by(name = name).first_or_404()
        return jsonify(result=[record.serialize])



@app.route('/v1/expenses/<int:id>', methods = ['PUT'])
def put(id):
        temp_json = request.get_json(force=True)
        estimated_costs = request.json['estimated_costs']
        record = Expenses.query.filter_by(id = id).first()
        record.estimated_costs = estimated_costs
        db.session.commit()
        return ""



@app.route('/v1/expenses/<int:id>', methods =['DELETE'])
def delete(id):
        record = Expenses.query.filter_by(id = id).delete()
        db.session.commit()
        return ""



if __name__ == "__main__" :
    db.create_all()
    app.run( host='0.0.0.0', debug = True)
