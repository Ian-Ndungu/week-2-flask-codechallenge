import random
from sqlalchemy import func
from flask import Flask 
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_database():
    with app.app_context():
        db.create_all()

        powers_data = [  
             {"name": "super strength", "description": "gives the wielder super-human strengths"},
            {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
            {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
            {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
        ]
        for power_info in powers_data:
            power = Power(**power_info)
            db.session.add(power)

        heroes_data = [
            {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
            {"name": "Doreen Green", "super_name": "Squirrel Girl"},
            {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
            {"name": "Janet Van Dyne", "super_name": "The Wasp"},
            {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
            {"name": "Carol Danvers", "super_name": "Captain Marvel"},
            {"name": "Jean Grey", "super_name": "Dark Phoenix"},
            {"name": "Ororo Munroe", "super_name": "Storm"},
            {"name": "Kitty Pryde", "super_name": "Shadowcat"},
            {"name": "Elektra Natchios", "super_name": "Elektra"}
        ]
        for hero_info in heroes_data:
            hero = Hero(**hero_info)
            db.session.add(hero)

        strengths = ["Strong", "Weak", "Average"]
        heroes = Hero.query.all()
        powers = Power.query.all()  # Added this line to get all powers
        for hero in heroes:
            for _ in range(0, 1 + random.randint(0, 2)):
                power = random.choice(powers)  # Randomly select a power
                if power not in hero.powers:  # Prevent duplicates
                    strength = random.choice(strengths)
                    hero_power = HeroPower(strength=strength, hero_id=hero.id, power_id=power.id)
                    db.session.add(hero_power)

        # Commit changes automatically using commit_on_teardown
        db.session.commit()

if __name__ == '__main__':
    seed_database()
