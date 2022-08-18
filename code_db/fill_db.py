from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from create_db import Roles, RolesCompilations
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


actors = tuple((name, None) for name in actors_parser())
actress = tuple((name, None) for name in actresses_parser())
heroes = tuple(characters_films_parser('heroes'))
villians = tuple(characters_films_parser('villians'))

roles_compilations = ('Актёры и актрисы', 'Персонажи фильмов')

if __name__ == '__main__':
    engine = create_engine(f'sqlite:///whoami.db', echo=True)
    with Session(engine) as session:
        session.add_all(add_roles_compilations(roles_compilations))
        session.add_all(add_roles(actors, 1))
        session.add_all(add_roles(actress, 1))
        session.add_all(add_roles(tuple(set(heroes + villians)), 2))
        session.commit()
