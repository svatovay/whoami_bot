from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PlayRoom(Base):
    __tablename__ = 'play_room'

    id = Column(Integer, primary_key=True)
    room_number = Column(Integer, unique=True)


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    play_room_id = Column(Integer, ForeignKey('play_room.id'), nullable=False)


class RolesCompilations(Base):
    __tablename__ = 'roles_compilations'

    id = Column(Integer, primary_key=True)
    comp_name = Column(String(20))


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role = Column(String(20))
    description = Column(String(200))
    roles_comp_id = Column(Integer, ForeignKey('roles_compilations.id'), nullable=False)


if __name__ == '__main__':
    engine = create_engine(f'sqlite:///whoami.db', echo=True)
    Base.metadata.create_all(engine)
