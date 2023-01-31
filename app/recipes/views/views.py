from flask import session, render_template, url_for, redirect, request, flash
from app.recipes import blp
from app.recipes.forms import AddRecipe, AddTag
from app.models import Recipe, Tag, Ingredient
from app import db

@blp.route('/addrecipe', methods=["GET","POST"])
def add_recipe():
    form = AddRecipe()
    if form.is_submitted():
        recipe = Recipe(name=form.recipe_name.data,description=form.recipe_description.data)
        recipe.tags = form.recipe_tags.data
        db.session.add(recipe)
        db.session.commit()
        for ingre in form.recipe_ingredients.data:
            new_ingredient = Ingredient(details=ingre['ingredient'],recipe_id=recipe.id)
            db.session.add(new_ingredient)
        db.session.commit()
        flash('Recipe added successfully.', category='alert-success')
        return redirect(url_for(f'recipes.recipe_view', recipe_id=recipe.id))
    return render_template('addrecipe.html', form=form)

@blp.route('/view/<recipe_id>')
def recipe_view(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return render_template('viewrecipe.html', recipe=recipe)

@blp.route('/addtag', methods=["GET","POST"])
def add_tag():
    form = AddTag()
    if form.validate_on_submit():
        tag = Tag(name=form.tag_name.data.replace(" ",""))
        db.session.add(tag)
        db.session.commit()
        form.tag_name.data = ""
        flash('Tag added successfully.',category='alert-success')
    return render_template('addtag.html', form=form)
    