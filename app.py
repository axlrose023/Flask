import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout
from sqlalchemy.orm import validates
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '997e10fd87eb39efe723a6f7f51867dad06877f2'
login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    text = db.Column(db.Text, nullable=True)

    # @validates('password')
    # def validates_password(self, value):
    #     if len(value) < 8:
    #         raise ValidationError('Password must be longer than 8')
    #     if not any(char.isupper() for char in value):
    #         raise ValidationError('Password must contain upper case')
    #     if not any(char.islower() for char in value):
    #         raise ValidationError('Password must contain lower case')


@app.route('/')
def home():  # put application's code here
    items = Item.query.order_by(Item.price).all()
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
        session.modified = True
    else:
        session['visits'] = 1
    return render_template('index.html', items=items, session=session['visits'])


@app.route('/buy/<int:id>')
def buy(id):  # put application's code here
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():  # put application's code here
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        description = request.form['description']
        password = request.form['password']
        password1 = request.form['password1']
        if password == password1:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already in use. Try another one')
                return redirect(url_for('register'))
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),
                            text=description)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация успешная\n Войдите в аккаунт')
                return redirect(url_for('login'))
            except:
                return 'Ошибка с базой данных'
        else:
            flash('Password dont match, try again')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST', 'GET'])
def login():  # put application's code here
    logout_user()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():  # put application's code here
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Получилась ошибка'
    else:
        return render_template('create.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        description = request.form['description']
        if not description:
            flash('Вы не изменили ничего')
            return redirect('/profile/edit')
        user = User.query.filter_by(email=current_user.email).first()
        if user is not None:
            user.text = description
            db.session.commit()
            flash('Успешно изменено')
            return redirect(url_for('edit'))
        else:
            print('Ошибка подключения бд')

    else:
        return render_template('edit_profile.html')


@app.route('/profile/passchange', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        password = request.form['password']
        password1 = request.form['password1']
        newpassword = request.form['newpassword']
        if password == password1:
            if newpassword != password:
                user = User.query.filter_by(email=current_user.email).first()
                user.password = generate_password_hash(newpassword, method='sha256')
                db.session.commit()
                flash('Successfully changed. Log in to your account')
                logout_user()
                return redirect(url_for('login'))
            else:
                flash("Новый пароль должен отличаться от старого. Придумайте новый.")
                return redirect(url_for('change_password'))
        else:
            flash("Проверьте правильность вводимых данных")
            return redirect(url_for('change_password'))
    else:
        return render_template('change_password.html')


@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)





if __name__ == '__main__':
    app.run(debug=True)
