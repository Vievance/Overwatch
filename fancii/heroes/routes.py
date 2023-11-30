from flask import jsonify, render_template, request, Blueprint, redirect, url_for
from fancii.models import db, Hero
from fancii.heroes.forms import HeroForm


heroes = Blueprint('heroes', __name__)

@heroes.route("/new", methods=['GET','POST'])
def new_hero():
    form = HeroForm()
    if form.validate_on_submit():
        hero = Hero(name=form.name.data, role=form.role.data, country=form.country.data, release_date=form.release_date.data)
        db.session.add(hero)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('new_hero.html', title='New Hero', form=form, legend='New Hero')

@heroes.route('/delete/<int:hero_id>', methods=['GET', 'DELETE'])
def delete_hero(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    db.session.delete(hero)
    db.session.commit()
    return jsonify({'message': f'Hero {hero_id} deleted successfully'})

@heroes.route('/get_form', methods=['GET'])
def get_form():
    hero_form = HeroForm()
    return render_template('hero_form.html', form=hero_form)

@heroes.route('/create_hero', methods=['POST'])
def create_hero():
    form = HeroForm(request.form)

    if form.validate():
        new_hero = Hero(name=form.name.data, role=form.role.data, country=form.country.data, release_date=form.release_date.data)
        db.session.add(new_hero)
        db.session.commit()

        return jsonify({'message': 'Hero created successfully', 'hero_id':new_hero.id}), 201
    
    else:
        errors = {field.name: field.errors for field in form}
        return jsonify({'message': 'Failed to create hero', 'errors': errors}), 400