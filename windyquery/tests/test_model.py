import asyncio

from windyquery import Model

loop = asyncio.get_event_loop()


def test_table_name(model):
    class User(Model):
        pass
    assert User.table == 'users'
    class AdminUser(Model):
        pass
    assert SearchTemplateSchedule.table == 'admin_users'
    class Custom(Model):
        table = 'my_custom'
    assert Custom.table == 'my_custom'

def test_empty_model(model):
    class User(Model):
        pass
    user = User()
    user.id = 8
    assert user.id == 8
    user = User(id=9, email='test@test.com')
    assert user.email == 'test@test.com'
    user = User({'id': 10, 'email': 'test@example.com'})
    assert user.email == 'test@example.com'
    user = User({'id': 10, 'email': 'test@example.com'}, email='testoveride@example.com')
    assert user.email == 'testoveride@example.com'

def test_find(model):
    class User(Model):
        pass
    user = loop.run_until_complete(User.find(2))
    assert user.email == 'test@example.com'
    users = loop.run_until_complete(User.find([1, 2]))
    assert len(users) == 2
    assert users[1].email == 'test@example.com' or users[1].email == 'test2@example.com'

def test_selected_colums(model):
    class User(Model):
        pass
    user = loop.run_until_complete(User.find(2).select('email'))
    assert user.email == 'test@example.com'
    assert not hasattr(user, 'admin')

def test_where(model):
    class User(Model):
        pass
    user = loop.run_until_complete(User.where("email", 'test@example.com').first())
    assert user.id == 2
    users = loop.run_until_complete(User.where("email", 'test@example.com'))
    assert len(users) == 1
    assert users[0].id == 2
    user = loop.run_until_complete(User.where("email", 'no_such_email').first())
    assert user is None
    users = loop.run_until_complete(User.where("email", 'no_such_email'))
    assert users == []

def test_where_none(model):
    class Card(Model):
        pass
    card = loop.run_until_complete(Card.where("board_id", None).first())
    assert card is None
    card = loop.run_until_complete(Card.where("board_id", None))
    assert card == []

def test_cls_id(model):
    class User(Model):
        pass
    assert User.id == 'id'
    class Country(Model):
        table = 'country'
    assert Country.id == 'numeric_code'

def test_save(model):
    class User(Model):
        pass
    user = loop.run_until_complete(User.where("email", 'test@example.com').first())
    new_val = 'north door' if user.password == 'south door' else 'south door'
    user.password = new_val
    user = loop.run_until_complete(user.save())
    assert user.password == new_val

def test_save_new(model):
    class User(Model):
        pass
    user = User(email='tmp@example.com', password='tmp_password')
    user = loop.run_until_complete(user.save())
    assert user.id > 0
    loop.run_until_complete(user.delete())
    user = loop.run_until_complete(User.find(user.id))
    assert user is None

def test_multi_results(model):
    class User(Model):
        pass
    users = loop.run_until_complete(User.where("password", 'secret'))
    assert len(users) == 2
    assert users[0].email == 'insert_multi_1'
    assert users[1].email == 'insert_multi_2'

def test_all(model):
    class Board(Model):
        pass
    results = loop.run_until_complete(Board.all())
    assert len(results) == 3
    assert results[1].location == 'bedroom'

def test_first_or_new(model):
    class AdminUser(Model):
        pass
    admin = loop.run_until_complete(AdminUser.where('id', 78901).where('name', 'not_exist_testing_name').first_or_new())
    assert admin is not None
    assert isinstance(admin, AdminUser)
    assert admin.id is None