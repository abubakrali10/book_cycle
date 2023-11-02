from bookcycle import app, bcrypt, db
from bookcycle.models import User, Book
from flask import render_template, flash, redirect, url_for, request
from bookcycle.auth import LoginForm, RegistrationForm, AddBookForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register/', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account successfully created!", 'success')
        return redirect(url_for("login"))
    return render_template('register.html', form=form)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash("You are logged in!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("email or password incorrect!", 'danger')
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_book/', methods=['GET', 'POST'])
@login_required
def addBook():
    add_book_form = AddBookForm()
    if add_book_form.validate_on_submit():
        book = Book(title=add_book_form.book_title.data,
                    author=add_book_form.book_author.data,
                    description=add_book_form.book_desc.data,
                    phone_number=add_book_form.contact_number.data,
                    book_image=add_book_form.book_image.data)
        db.session.add(book)
        db.session.commit()
        flash('Your book is published!', 'success')
        return redirect(url_for('/home/'))
    return render_template('add_book.html', add_book_form=add_book_form)