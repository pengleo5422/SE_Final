from .. import db

class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True)
    idPhoto = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    authenticationStatus = db.Column(db.Boolean, nullable=False, default=False)
    profileData = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    notifications = db.relationship('Notification', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    issues = db.relationship('Issue', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
