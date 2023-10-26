from typing import Any

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base: Any = declarative_base()


class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    indicators = relationship('Indicators', back_populates='material', cascade='all, delete')


class Indicators(Base):
    __tablename__ = 'indicators'

    id = Column(Integer, primary_key=True, index=True)
    iron_content = Column(Float)
    silicon_content = Column(Float)
    aluminum_content = Column(Float)
    calcium_content = Column(Float)
    sulfur_content = Column(Float)
    upload_date = Column(Date)
    material_id = Column(Integer, ForeignKey('material.id'))
    material = relationship('Material', back_populates='indicators')
