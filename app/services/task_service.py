from app import db
from app.models import Task

def get_user_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return [
        {
            'id': task.id,
            'title': task.title,
            'done': task.done,
            'category': task.category.name if task.category else None
        }
        for task in tasks
    ]

def create_task_for_user(user_id, data):
    task = Task(
        title=data['title'],
        user_id=user_id,
        category_id=data.get('category_id')
    )
    db.session.add(task)
    db.session.commit()
    return {"msg": "Task created"}, 201
