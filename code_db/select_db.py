from sqlalchemy import select
from session_db import craft_session
from create_db import RolesCompilations, Roles


@craft_session
def select_roles_comp(session, *args, **kwargs):
    stmt = select(RolesCompilations)
    return tuple(roles_comp for roles_comp in session.scalars(stmt))


@craft_session
def select_roles(session, roles_comp_id, *args, **kwargs):
    stmt = select(Roles).where(Roles.roles_comp_id == roles_comp_id)
    return tuple((el.role, el.description) for el in session.scalars(stmt))

