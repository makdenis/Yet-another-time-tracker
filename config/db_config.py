"""
Created by anthony on 15.10.17
db_config
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

import g


log = logging.getLogger(__name__)


DB_NAME = 'yatt_db'
DB_USER = 'yatt_user'
DB_PASSWORD = 'root'
DB_HOST = 'localhost' if (g.dev_mode or g.test_mode) else 'postgres'    # container name from docker-compose
DB_PORT = 5432


connection_string = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db_engine = create_engine(connection_string)

Session = sessionmaker(bind=db_engine, expire_on_commit=False, autocommit=True)

Base = declarative_base()


def init_db():
    log.info('> Starting database')
    log.info(f'Connecting to {DB_HOST}:{DB_PORT}')

    import models.user, models.project, models.task
    try:
        Base.metadata.create_all(bind=db_engine)

    except Exception as e:
        log.error('Could not start database')
        raise e

    else:
        log.info('Database has started')
