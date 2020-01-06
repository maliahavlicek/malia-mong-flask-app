import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# before PROD put username password into env variables
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:2019Winter@mhavlicfirstcluster-pielp.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template('tasks.html', tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('add_tasks.html', categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    # some validation in the future here and html
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    # convert task_id to bson object so we can use the task
    the_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edit_task.html', task=the_task, categories=all_categories)


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
                 {
                     'task_name': request.form.get('task_name'),
                     'category_name': request.form.get('category_name'),
                     'task_description': request.form.get('task_description'),
                     'due_date': request.form.get('due_date'),
                     'is_urgent': request.form.get('is_urgent')
                 })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    """ FUTURE: COULD update to have is_complete being set then update get_tasks to only show tasks that are not completed"""
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    # convert task_id to bson object so we can use the task
    the_cat = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    return render_template('edit_category.html', category=the_cat)


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    cat = mongo.db.categories
    cat.update({'_id': ObjectId(category_id)},
                 {
                     'category_name': request.form.get('category_name')
                 })
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('add_categories.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    categories.insert_one(request.form.to_dict())
    # some validation in the future here and html
    return redirect(url_for('get_categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    """ FUTURE: COULD update to have is_complete being set then update get_tasks to only show tasks that are not completed"""
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))



if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=True)
