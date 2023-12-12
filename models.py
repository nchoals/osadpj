from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(10))
    password = db.Column(db.String(100))
    confirm_password = db.Column(db.String(100))
    # Add a field for storing the user's unique secret key

    def __init__(self, first_name, last_name, username, email, date_of_birth, password, confirm_password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.date_of_birth = date_of_birth
        self.password = password
        self.confirm_password = confirm_password

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_first_name(self):
        return self.first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_last_name(self):
        return self.last_name

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_date_of_birth(self, date_of_birth):
        self.date_of_birth = date_of_birth

    def get_date_of_birth(self):
        return self.date_of_birth

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def set_confirm_password(self, confirm_password):
        self.confirm_password = confirm_password

    def get_confirm_password(self):
        return self.confirm_password


# # ============ CHATROOM ==============
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False)