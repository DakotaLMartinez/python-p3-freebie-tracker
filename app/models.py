#!/usr/bin/env python3

from sqlalchemy import (ForeignKey, Column, String, Integer, Table)
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


Base = declarative_base()

freebie_association = Table(
    "company_dev_freebies",
    Base.metadata,
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("dev_id", ForeignKey("devs.id"), primary_key=True),
)

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    # relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')


    # aggregate methods
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."

    def __repr__(self):
        return f'<Freebie {self.item_name} d:{self.dev_id} c:{self.company_id}>'
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # relationships
    freebies = relationship('Freebie', back_populates='company')
    devs = association_proxy('freebies', 'dev')

    # aggregate methods
    @classmethod
    def oldest_company(cls):
        engine = create_engine('sqlite:///freebies.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        company = session.query(Company).order_by(Company.founding_year).first()
        session.close()
        return company

    def give_freebie(self, dev, item_name, value):
        return Freebie(dev_id=dev.id, company_id=self.id, item_name=item_name, value=value)

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    # relationships
    freebies = relationship('Freebie', back_populates='dev')
    companies = association_proxy('freebies', 'company')

    # aggregate methods
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
        else:
            raise ValueError('You can only give away a freebie that belongs to you')

    def __repr__(self):
        return f'<Dev {self.name}>'
