import Course
from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES

table_name: str = "sections"                 # The physical name of this table
# Find out whether the user is introspecting or starting over
introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    class Section(Base):
        """(ADD DESCRIPTION)"""
        __tablename__ = table_name


        departmentAbbreviation: Mapped[str]
        courseNumber: Mapped[int]

        sectionNumber: Mapped[int]
        semester: Mapped[str]
        sectionYear: Mapped[int]
        building: Mapped[str]
        room: Mapped[int]
        schedule: Mapped[str]
        startTime: Mapped[time]
        instructor: Mapped[str]

        def __init__(self):
            pass

elif introspection_type == INTROSPECT_TABLES:
    class Section(Base):
        __table__ = Table(table_name, Base.metadata, autoloud_with=engine)
        """Not sure what else goes in here"""

        def __init__(self):
            pass
def set_course(self, course: Course):
    pass

def __str__(self):
    pass


setattr(Section, '__str__', __str__)
