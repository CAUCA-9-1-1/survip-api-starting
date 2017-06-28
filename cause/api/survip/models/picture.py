from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, LargeBinary, String

Base = declarative_base()


class Picture(Base):
   __tablename__ = "tbl_picture"

   id_picture = Column(String(36), primary_key=True)
   picture = Column(LargeBinary)