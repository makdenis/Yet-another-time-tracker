"""
Created by anthony on 05.11.17
service_utils

only generics should be here
"""
from config.db_config import Session
import logging


log = logging.getLogger(__name__)


def find_all(entity_class):
    """
    Return all entries of class that are not deleted (flag is_active=True)
    """
    db_session = Session()
    try:
        all_entries = db_session.query(entity_class) \
            .filter_by(is_active=True)
        return all_entries

    except Exception as e:
        log.critical(f'Rolling back and closing "find_all" session for entity {entity_class}: {e}')
        db_session.rollback()
        return []

    finally:
        db_session.close()


def find_active_and_inactive(entity_class):
    """
    Return all entries of class. Deleted entries are included
    """
    db_session = Session()
    try:
        all_entries = db_session.query(entity_class)
        return all_entries

    except Exception as e:
        log.critical(f'Rolling back and closing "find_all" session for entity {entity_class}: {e}')
        db_session.rollback()
        return []

    finally:
        db_session.close()


def find_one_by_id(id_value, entity_class):
    """
    While assuming _id is unique pre class(table), get entity of class by _id
    """
    id_int = None
    try:
        id_int = int(id_value)

    except ValueError as e:
        err_cause = 'Provided value is not valid id'
        raise ValueError(err_cause)

    db_session = Session()
    try:
        entity_by_id = db_session.query(entity_class) \
            .filter_by(id=id_int) \
            .first()
        # here can be none if nothing found!
        return entity_by_id

    except Exception as e:
        log.critical(f'Rolling back and closing "find_one_by_id" session '
                     f'for id ({id_int}) of {entity_class} class: {e}')
        db_session.rollback()
        return None

    finally:
        db_session.close()


def save(entity):
    """
    Insert entity into db
    """
    db_session = Session()
    db_session.autocommit = False
    try:
        db_session.add(entity)
        db_session.commit()
        return entity

    except Exception as e:
        log.critical(f'Rolling back and closing "save" session for entity {entity}: {e}')
        db_session.rollback()
        return entity

    finally:
        db_session.close()


def flush(entity):
    """
    Prepare entity for insertion (fill _id attribute but do _not_ insert)
    """
    db_session = Session()
    try:
        db_session.add(entity)
        db_session.flush()
        return entity

    except Exception as e:
        log.critical(f'Rolling back and closing "flush" session for entity {entity}: {e}')
        db_session.rollback()
        return entity

    finally:
        db_session.close()
