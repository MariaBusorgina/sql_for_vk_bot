import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from model import create_table, Owner, Photo, User

localhost = "5432"
password = '5240'
name_DB = "users"


# Функция создания соединения
def connect(localhost, password, name_DB):
    # Создаем движок
    engine = sq.create_engine(f"postgresql://postgres:{password}@localhost:{localhost}/{name_DB}")
    # Создаем класс для создания сессии
    Session = sessionmaker(bind=engine)
    # Создаем экземпляр класса
    session = Session()
    create_table(engine)
    return session


session = connect(localhost="5432", password="5240", name_DB="users")


# Функция добавления контакта в просмотренные
def add_viewed(vk_id, name, last_name, link_profile, owner_id):
    # Сохранение всех просмотренных user-ов - создаем экземпляр класса, передаем необходимые данные для заполнения таблицы User.
    user = User(vk_id=vk_id, name=name, last_name=last_name, link_profile=link_profile, owner=owner_id,
                is_favorites=False, is_in_black_list=False)
    session.add(user)
    session.commit()


# Функция добавления фото
def add_photos(user_id, link_1, link_2, link_3):
    photo = Photo(link_photo_1=link_1, link_photo_2=link_2, link_photo_3=link_3, user=user_id)
    session.add(photo)
    session.commit()


# Функция добавления контакта в избранные
def add_favorites(vk_id, link_1, link_2, link_3):
    # Находим по id_vk контакт в таблице просмотренных, добавляем в избранные, меняя is_favorites на True
    user = session.query(User).filter(User.vk_id == vk_id).one()
    add_photos(user_id=user, link_1=link_1, link_2=link_2, link_3=link_3)
    session.query(User).filter(User.vk_id == vk_id).update({'is_favorites': True})
    session.commit()


# Функция добавления контакта в BlackList
def add_in_black_list(vk_id):
    # Находим по id_vk контакт в таблице просмотренных, добавляем в BlackList, меняя is_in_black_list на True
    session.query(User).filter(User.vk_id == vk_id).update({'is_in_black_list': True})
    session.commit()


# Функция получения всех просмотренных контактов в формате списка кортежей. Вывод: [(vk_id), (vk_id)].
def get_all_viewed_users():
    return [c for c in session.query(User.vk_id).all()]


# Функция получения всех избранных контактов в формате списка кортежей. Вывод: [(vk_id), (vk_id)].
def get_all_favorite_users():
    return [c for c in session.query(User.vk_id).filter(User.is_favorites).all()]


# Функция получения всех контактов из BlackList в формате списка кортежей. Вывод: [(vk_id), (vk_id)].
def get_all_users_in_black_list():
    return [c for c in session.query(User.vk_id).filter(User.is_in_black_list).all()]


# Проверить наличие пользователя в таблице users
# Возвращает true/false
def check_user(vk_id):
    return bool(session.query(User.vk_id, User.name).filter(User.vk_id == vk_id).all())


# Функция добавления владельца в БД
def add_owner(vk_id, name):
    owner = Owner(vk_id=vk_id, name=name)
    session.add(owner)
    session.commit()


# Функция проверки владельца
def check_owner(vk_id, name):
    # Если владелец есть в БД - возвращает True
    if bool(session.query(Owner.vk_id).filter(Owner.vk_id == vk_id).one()):
        return session.query(Owner).filter(Owner.vk_id == vk_id).one()
    # Если владельца нет в БД - добавляет его в БД и возвращает True
    else:
        add_owner(vk_id, name)
        return True


# Получить данные из таблицы
def select_date_from_table():
    # Непонятно какие данные
    pass


# Проверяет соответствие полей таблицы user и обновляет при несоответсвии
def heck_and_update_param_user(id_user):
    # Непонятно что проверять
    pass


session.commit()

session.close()
