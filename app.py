from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todolist'
mongo = PyMongo(app)


@app.route('/')
def index():
    tasks = mongo.db.tasks.find()
    return render_template('index.html', tasks=tasks)
    # return render_template('auth/register.html')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    status = request.form.get('status')
    started_date = datetime.strptime(request.form.get('started_date'), '%Y-%m-%d')
    ended_date = datetime.strptime(request.form.get('ended_date'), '%Y-%m-%d')

    task = {
        'title': title,
        'description': description,
        'status': status,
        'started_date': started_date,
        'ended_date': ended_date
    }

    mongo.db.tasks.insert_one(task)
    return redirect(url_for('index'))


@app.route('/edit/<id>')
def edit(id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(id)})
    return render_template('edit.html', task=task)


@app.route('/update_task/<id>', methods=['POST'])
def update_task(id):
    title = request.form.get('title')
    description = request.form.get('description')
    status = request.form.get('status')
    started_date = datetime.strptime(request.form.get('started_date'), '%Y-%m-%d')
    ended_date = datetime.strptime(request.form.get('ended_date'), '%Y-%m-%d')

    mongo.db.tasks.update_one({'_id': ObjectId(id)}, {
        '$set': {
            'title': title,
            'description': description,
            'status': status,
            'started_date': started_date,
            'ended_date': ended_date
        }
    })

    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete_task(id):
    mongo.db.tasks.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
