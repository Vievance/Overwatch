from flask import render_template, request, Blueprint
from fancii.models import Hero

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    heroes = Hero.query.order_by(Hero.name.asc())
    return render_template('home.html', heroes=heroes)

