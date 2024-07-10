import tornado.ioloop
import tornado.web
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///tasks.db"
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class TaskHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self):
        # No body
        self.set_status(204)
        self.finish()

    def get(self):
        tasks = session.query(Task).all()
        self.write(json.dumps([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        } for task in tasks]))

    def post(self):
        data = json.loads(self.request.body)
        task = Task(
            title=data['title'],
            description=data['description'],
            completed=data.get('completed', False)
        )
        session.add(task)
        session.commit()
        self.set_status(201)
        self.write({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        })

class SingleTaskHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self, task_id):
        # No body
        self.set_status(204)
        self.finish()

    def put(self, task_id):
        data = json.loads(self.request.body)
        task = session.query(Task).get(task_id)
        task.title = data['title']
        task.description = data['description']
        task.completed = data['completed']
        session.commit()
        self.write({'status': 'success'})

    def delete(self, task_id):
        task = session.query(Task).get(task_id)
        session.delete(task)
        session.commit()
        self.write({'status': 'success'})

def make_app():
    return tornado.web.Application([
        (r"/tasks", TaskHandler),
        (r"/tasks/([0-9]+)", SingleTaskHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()




