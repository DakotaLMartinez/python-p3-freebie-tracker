#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dev, Company, Freebie


if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Dev).delete()
    session.query(Company).delete()
    session.query(Freebie).delete()
    # Script goes here!


    # Devs
    dakota = Dev(name='Dakota')
    amelie = Dev(name='Amelie')

    # Companies
    apple = Company(name='Apple', founding_year=1976)
    microsoft = Company(name='Microsoft', founding_year=1975)

    session.add_all([dakota, amelie, apple, microsoft])
    session.commit()

    airtags = Freebie(item_name="airtags", value=40, dev_id=dakota.id, company_id=apple.id)

    session.add(airtags)
    session.commit()
    # Freebies