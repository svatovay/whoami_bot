from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .session_db import craft_session
from .selects_db import select_room
from .create_db import Roles, RolesCompilations, PlayRoom, Player
from parsers import actors_parser, actresses_parser, characters_films_parser


def add_roles_compilations(input_tuple: tuple) -> list:
    result_list = []
    for comp_name in input_tuple:
        _ = RolesCompilations(
            comp_name=comp_name,
        )
        result_list.append(_)
    return result_list


def add_roles(input_tuple: tuple, roles_comp_id) -> list:
    result_list = []
    for role in input_tuple:
        _ = Roles(
            role=role[0],
            description=role[1],
            roles_comp_id=roles_comp_id,
        )
        result_list.append(_)
    return result_list


@craft_session
def add_room(session, input_room, *args, **kwargs):
    _ = PlayRoom(
        room_number=input_room
    )
    session.add(_)


@craft_session
def add_player(session, game_info, *args, **kwargs):
    _ = Player(
        name=game_info['player_name'],
        role_id=game_info['player_role'],
        play_room_id=select_room(game_info['room_number']).id,
    )
    session.add(_)


# actors = tuple((name, None) for name in actors_parser())
# actress = tuple((name, None) for name in actresses_parser())
# heroes = tuple(characters_films_parser('heroes'))
# villians = tuple(characters_films_parser('villians'))
#
# roles_compilations = ('Актёры и актрисы', 'Персонажи фильмов')
#
# if __name__ == '__main__':
#     engine = create_engine(f'sqlite:///code_db/whoami.db', echo=True)
#     with Session(engine) as session:
#         session.add_all(add_roles_compilations(roles_compilations))
#         session.add_all(add_roles(actors, 1))
#         session.add_all(add_roles(actress, 1))
#         session.add_all(add_roles(tuple(set(heroes + villians)), 2))
#         session.commit()
