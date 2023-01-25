from flask import session, render_template, url_for, redirect, request, flash
from app.recipes.views import blp as recipe_blp
from app.recipes.forms import AddRecipe
from app.models import Recipe
from app import db

@recipe_blp.route('/addrecipe')
def add_recipe():
    form = AddRecipe()
    if form.validate_on_submit:
        recipe = Recipe(name=form.recipe_name.data, description=form.recipe_description.data, tags=form.recipe_tags.data)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added successfully.', category='alert-success')
        return url_for(f'recipe.recipe_view/{recipe.id}')
    return render_template('addrecipe.html')

@recipe_blp.route('/view/<recipe_id>')
def recipe_view(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return render_template('viewrecipe.html', recipe=recipe)