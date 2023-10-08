
from flask import Flask, jsonify
from flask import Flask, request
from flask_migrate import Migrate
from models import db,Hero,Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:hero_id>')
def get_hero(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    hero_data = {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
    return jsonify(hero_data)

@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    power_list = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:power_id>')
def get_power(power_id):
    power = Power.query.get_or_404(power_id)
    power_data = {"id": power.id, "name": power.name, "description": power.description}
    return jsonify(power_data)

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if "description" in data:
        power.description = data["description"]
    
    try:
        db.session.commit()
        return jsonify({"id": power.id, "name": power.name, "description": power.description})
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
     with app.app_context():
        db.create_all()
        app.run(port=5555)
