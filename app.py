from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/database-name'
db = SQLAlchemy(app)


# Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"{self.id}"


db.create_all()


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)


@app.route('/api/v1/username', methods=['GET'])
def index():
    get_users = User.query.all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"list users ": users}))


@app.route('/api/v1/username/<id>', methods=['GET'])
def get_user_by_id(id):
    get_user = User.query.get(id)
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user ": user}))


@app.route('/api/v1/username/<id>', methods=['PUT'])
def update_user_by_id(id):
    data = request.get_json()
    get_user = User.query.get(id)
    if data.get('username'):
        get_user.username = data['username']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema(only=['id', 'username'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user ": user}))


@app.route('/api/v1/username/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    get_user = User.query.get(id)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/v1/username', methods=['POST'])
def create_todo():
    data = request.get_json()
    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    return make_response(jsonify({"user ": result}), 200)


if __name__ == "__main__":
    app.run(debug=True)