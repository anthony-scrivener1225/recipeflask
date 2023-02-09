from flask import session, render_template, url_for, redirect, request, flash
from app.recipes import blp
from flask_login import login_required
from app.recipes.forms import AddRecipe, AddTag, UpdateRecipe
from app.models import Recipe, Tag, Ingredient, Direction, recipe_tags, compare_hash
from app import db
from flask_login import current_user
from random import choice
from config import basedir
import os

@blp.route('/addrecipe', methods=["GET","POST"])
@login_required
def add_recipe():
    form = AddRecipe()
    if form.is_submitted():
        form_description = str(form.recipe_description.data)
        recipe_desc = form_description if len(form_description) >= 64 else form_description+((64 - len(form_description)) * " ")
        recipe = Recipe(name=form.recipe_name.data,description=recipe_desc,created_by=current_user.id)
        recipe.tags = form.recipe_tags.data
        db.session.add(recipe)
        db.session.commit()
        uploaded_file = form.file.data
        if uploaded_file.filename != '':
            sep_file = os.path.splitext(uploaded_file.filename)[1]
            recipe.image = str(recipe.id)+sep_file
            uploaded_file.save(os.path.join(basedir+'/app/recipes/static/recipes/'+recipe.image))
        for ingre in form.recipe_ingredients.data:
            new_ingredient = Ingredient(details=ingre['ingredient'],recipe_id=recipe.id)
            db.session.add(new_ingredient)
        for direct in form.recipe_directions.data:
            new_direction = Direction(details=direct['direction'],recipe_id=recipe.id)
            db.session.add(new_direction)
        db.session.commit()
        flash('Recipe added successfully.', category='alert-success')
        return redirect(url_for(f'recipes.recipe_view', recipe_id=recipe.id))
    return render_template('addrecipe.html', form=form)

@blp.route('/view')
@blp.route('/view/<recipe_id>')
def recipe_view(recipe_id=None):
    if recipe_id == None:
        return redirect(url_for('recipes.recipe_view', recipe_id=choice(Recipe.query.all()).id))
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return render_template('viewrecipe.html', recipe=recipe)

@blp.route('/deleterecipe')
@blp.route('/deleterecipe/<int:recipe_id>')
def delete_recipe(recipe_id=None):
    if recipe_id == None:
        return render_template('myrecipes.html')

@blp.route('/updaterecipe/<recipe_id>', methods=["GET","POST"])
def update_recipe(recipe_id):
    form = UpdateRecipe()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if form.is_submitted():
        form_description = str(form.recipe_description.data)
        recipe_desc = form_description if len(form_description) >= 64 else form_description+((64 - len(form_description)) * " ")
        recipe.description = recipe_desc
        recipe.tags = form.recipe_tags.data
        if form.file.data != None:
            uploaded_file = form.file.data
            if uploaded_file.filename != '':
                sep_file = os.path.splitext(uploaded_file.filename)[1]
                recipe.image = str(recipe.id)+sep_file
                uploaded_file.save(os.path.join(basedir+'/app/recipes/static/recipes/'+recipe.image))
        ingre_details = [in_detail.details for in_detail in recipe.ingredients]
        form_ingredients = [ingre['ingredient'] for ingre in form.recipe_ingredients.data]
        for ingre in form_ingredients:
            if ingre in ingre_details:
                ingre_details.pop(ingre_details.index(ingre))
                form_ingredients.pop(form_ingredients.index(ingre))
        if len(ingre_details) < len(form_ingredients):
            for i in range(len(form_ingredients)-len(ingre_details)):
                new_ing = Ingredient(details=form_ingredients[0],recipe_id=recipe.id)
                db.session.add(new_ing)
                form_ingredients.pop(0)
        elif len(form_ingredients) < len(ingre_details):
            for i in range(len(ingre_details)-len(form_ingredients)):
                db.session.delete(Ingredient.query.filter_by(details=ingre_details[0]).first())
                ingre_details.pop(0)
        for ingre in form_ingredients:
            updated_ingre = Ingredient.query.filter_by(details=ingre_details[0].first())
            updated_ingre.details = ingre
            db.session.add(updated_ingre)
            ingre_details.pop(0)

#####################################################################            
##### Same logic used by ingredients and updated for directions #####
#####################################################################   
        
        direct_details = [direct_detail.details for direct_detail in recipe.directions]
        form_directions = [direct['direction'] for direct in form.recipe_directions.data]
        for direct in form_directions:
            if direct in form_directions:
                direct_details.pop(direct_details.index(direct))
                form_directions.pop(form_directions.index(direct))
        if len(direct_details) < len(form_directions):
            for i in range(len(form_directions)-len(direct_details)):
                new_direct = Direction(details=form_directions[0],recipe_id=recipe.id)
                db.session.add(new_direct)
                form_directions.pop(0)
        elif len(form_directions) < len(direct_details):
            for i in range(len(direct_details)-len(form_directions)):
                db.session.delete(Direction.query.filter_by(details=direct_details[0]).first())
                direct_details.pop(0)
        for direct in form_directions:
            updated_dir = Direction.query.filter_by(details=direct_details[0].first())
            updated_dir.details = direct
            db.session.add(updated_dir)
            ingre_details.pop(0)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipes.recipe_view', recipe_id=recipe.id))
    return render_template('updaterecipe.html', recipe=recipe)



@blp.route('/<tag>')
def recipe_by_tag(tag=None):
    tag_name = str(tag).capitalize()
    recipe_tag = Tag.query.filter_by(name=tag_name).first()
    if recipe_tag != None and recipe_tag != '':
        tagged_recipes = Recipe.query.join(recipe_tags).join(Tag).filter(Tag.name == tag_name).all()
        return render_template('recipebytag.html', tagged_recipes=tagged_recipes, tag_name=tag_name)
    else:
        return redirect(url_for('recipes.add_tag', search_tag=tag_name))


@blp.route('/addtag', methods=["GET","POST"])
@blp.route('/addtag/<search_tag>', methods=['GET','POST'])
@login_required
def add_tag(search_tag=None):
    form = AddTag()
    if form.validate_on_submit():
        tag = Tag(name=form.tag_name.data.replace(" ",""))
        db.session.add(tag)
        db.session.commit()
        form.tag_name.data = ""
        flash('Tag added successfully.',category='alert-success')
    return render_template('addtag.html', form=form, search_tag=search_tag)
    