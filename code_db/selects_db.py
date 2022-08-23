from sqlalchemy import select
from .session_db import craft_session
from .create_db import RolesCompilations, Roles, PlayRoom, Player


@craft_session
def select_roles_comps(session, *args, **kwargs):
    stmt = select(RolesCompilations)
    return session.scalars(stmt).all()


@craft_session
def select_roles(session, roles_comp_id, *args, **kwargs):
    stmt = select(Roles).where(Roles.roles_comp_id == roles_comp_id)
    return session.scalars(stmt).all()


@craft_session
def select_players(session, input_room, *args, **kwargs):
    stmt = select(Player).where(Player.play_room_id == select_room(input_room).id)
    return session.scalars(stmt).all()


@craft_session
def select_room(session, room_number, *args, **kwargs):
    stmt = select(PlayRoom).where(PlayRoom.room_number == room_number)
    return session.scalar(stmt)


@craft_session
def select_role(session, role_id, *args, **kwargs):
    stmt = select(Roles).where(Roles.id == role_id)
    return session.scalar(stmt)
