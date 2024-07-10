import json
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from db import get_session
from models import Task
from validations import validate_task, jsonschema

class TaskHandler(tornado.web.RequestHandler):
    def get(self):
        session = get_session()
        tasks = session.query(Task).all()
        self.write(json.dumps([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        } for task in tasks]))

    def post(self):
        try:
            data = json.loads(self.request.body)
            validate_task(data)
            session = get_session()
            task = Task(
                title=data['title'],
                description=data['description'],
                completed=data.get('completed', False)
            )
            session.add(task)
            session.commit()
            self.set_status(201)
            self.write({'id': task.id})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON'})
        except jsonschema.ValidationError as e:
            self.set_status(400)
            self.write({'error': str(e)})

class SingleTaskHandler(tornado.web.RequestHandler):
    def put(self, task_id):
        try:
            data = json.loads(self.request.body)
            validate_task(data)
            session = get_session()
            task = session.query(Task).get(task_id)
            if not task:
                self.set_status(404)
                self.write({'error': 'Task not found'})
                return
            task.title = data['title']
            task.description = data['description']
            task.completed = data['completed']
            session.commit()
            self.write({'status': 'success'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON'})
        except jsonschema.ValidationError as e:
            self.set_status(400)
            self.write({'error': str(e)})

    def delete(self, task_id):
        try:
            session = get_session()
            task = session.query(Task).get(task_id)
            if not task:
                self.set_status(404)
                self.write({'error': 'Task not found'})
                return
            session.delete(task)
            session.commit()
            self.write({'status': 'success'})
        except NoResultFound:
            self.set_status(404)
            self.write({'error': 'Task not found'})
