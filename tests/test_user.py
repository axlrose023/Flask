import requests
from flask_login import login_user
from werkzeug.security import generate_password_hash

from app import User, db


# new_user = User(email='sloboda277@gmail.com', name='axlrose0231',
#    password=generate_password_hash('qwerty0192', method='sha256'),
#    text='description')
# db.session.commit()

def test_user_existance():
    user = User.query.filter_by(email='sloboda274@gmail.com').first()
    assert user is not None
    assert user.name == 'axlrose023'


def test_user_register():
    user = User.query.filter_by(email='sloboda278@gmail.com').first()
    db.session.delete(user)
    db.session.commit()
    user = User(name='axlrose023', password=generate_password_hash('qwerty0192', method='sha256'),
                email='sloboda278@gmail.com')
    db.session.add(user)
    db.session.commit()
    user1 = User.query.filter_by(email='sloboda278@gmail.com').first()
    assert user1 is not None
