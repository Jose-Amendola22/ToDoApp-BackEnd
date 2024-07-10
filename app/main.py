import tornado.ioloop
import tornado.web
import json
import jsonschema
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db import get_session
from validations import validate_task  
from models import Task

#Tenemos la url de la base de datos
DATABASE_URL = "sqlite:///tasks.db"
Base = declarative_base()


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

#Esta clase se usa para las llamadas a la API que sean de varios tipos de tasks
class TaskHandler(tornado.web.RequestHandler):
    # El famoso CORS
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()


    def get(self):
        #Función sencilla para obtener todos los objetos en la base de datos
        session = get_session()
        tasks = session.query(Task).all()
        self.write(json.dumps([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        } for task in tasks]))

    def post(self):
        #Función para agregar un objeto a la base de datos
        try:
            data = json.loads(self.request.body)
            #Aquí es donde se llama a validar
            validate_task(data)  
            #Aquí se pide la sesión que del archivo bd
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

#Funciones de la api para unicamente un task
class SingleTaskHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self, task_id):
        self.set_status(204)
        self.finish()

    def put(self, task_id):
        try:
            data = json.loads(self.request.body)
            #Se valida que los datos tengan sentido
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

def make_app():
    #Aquí es donde se hace el ruteo 
    return tornado.web.Application([
        (r"/tasks", TaskHandler),
        (r"/tasks/([0-9]+)", SingleTaskHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()





