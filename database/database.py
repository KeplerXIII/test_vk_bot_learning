import sqlalchemy as sq
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def drop_tables(engine) -> None:
    Base.metadata.drop_all(engine)


def create_tables(engine) -> None:
    Base.metadata.create_all(engine)

def status_filler(session) -> None:
    session.add(Status(name='favorite'))
    session.add(Status(name='black list'))
    session.commit()

class Status(Base):
    __tablename__ = 'status'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)


class Preferences(Base):
    __tablename__ = 'preferences'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, sq.ForeignKey('user.vk_id'))
    watched_vk_id = sq.Column(sq.Integer)
    status_id = sq.Column(sq.Integer, sq.ForeignKey('status.id'))



if __name__ == '__main__':
    pass


    #     # Создаём движок
    #     engine = sq.create_engine(DSN)
    #
    #     # Удаляем всё, если надо
    #     drop_tables(engine)
    #
    #     # Создаём классы, то есть таблицы.
    #     create_tables(engine)
    #
    #     # Открываем сессию
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #
    #     # Наполняем полами
    #     gender_list = ["Male", "Female"]
    #     gender_filler(session, gender_list)
    #
    #     # Наполняем статусами
    #     status_list = ["unwatched", "watched", "favorite", "blacklist"]
    #     status_filler(session, status_list)
    #
    #     # Пример добавления
    #     account = Accounts(vk_id=1, name='Vladimir', surname='Putin', age=30, gender_id=1, city='St. Pet',
    #                       profile_link='www.leningrad.ru', status_id=1)
    #     session.add(account)
    #     session.commit()
    #
    #     # если нужны данные cо статусами 1
    #     request = session.query(Accounts).filter_by(status_id=1).all()
    #     for i in request:
    #         pass
    #
    #     #если нужна одна запись
    #     request = session.query(Accounts).filter_by(status_id=1).one()
    #
    #     # если нужно изменить данные в определенной записи
    #     status_changer(session, vk_id=1, new_status_id=2)
    #
    #     # Закрываем сессию
    #     session.close()
