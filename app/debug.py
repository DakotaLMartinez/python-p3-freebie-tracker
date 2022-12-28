#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    apple = session.query(Company).first()
    microsoft = session.query(Company).where(Company.name == 'Microsoft').first()
    dakota = session.query(Dev).first()
    amelie = session.query(Dev).where(Dev.name == 'Amelie').first()
    airtags = session.query(Freebie).first()

    import ipdb; ipdb.set_trace()
