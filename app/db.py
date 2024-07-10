from sqlalchemy.orm import sessionmaker
from models import engine

Session = sessionmaker(bind=engine)

#Aquí se guarda la sesión a la base de datos para evitar redundancia a la hora de hacer llamadas
def get_session():
    return Session()
