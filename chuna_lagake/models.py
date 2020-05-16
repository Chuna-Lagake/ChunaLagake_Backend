from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from chuna_lagake import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	password = db.Column(db.String(256), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	feedbacks = db.relationship('Feedback', backref='user',lazy=True)
	entries = db.relationship('Entry', backref='user',lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')
	
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except :
			return None
		return User.query.get(user_id)	

	def __repr__ (self):
		return f"User('{self.username}','{self.password}','{self.email}')"

class Feedback(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	feedback = db.Column(db.Text, nullable=False)

	def __repr__ (self):
		return f"Feedback('{User.query.get(self.user_id).username}','{self.feedback}')"

class Menu(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, unique=True)
	image = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=False)
	entries = db.relationship('Entry', backref='product', lazy=True)

	def __repr__ (self):
		return f"Item('{self.name}','{self.description}','{self.image}')"

class Entry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
	status = db.Column(db.Boolean)
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__ (self):
		return f"Entry('{self.user.username}','{self.product.name}','{self.status}','{self.timestamp}')"	