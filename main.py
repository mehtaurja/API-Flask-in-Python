from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return redirect('/friends')

@app.route('/')
@auth.login_required
def login():
    return redirect('/friends')

db = SQLAlchemy(app)

class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Name %r>' % self.id

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
	friend_to_delete = Friends.query.get_or_404(id)
	try:
		db.session.delete(friend_to_delete)
		db.session.commit()
		return redirect('/friends')
	except:
		return "There was a problem in deleting that friend.."



@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	friend_to_update = Friends.query.get_or_404(id)
	if request.method == "POST":
		friend_to_update.name = request.form['name']
		try:
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was a problem in updating that friend..."
	else:
		return render_template('update.html', friend_to_update=friend_to_update)


@app.route('/friends', methods=['POST', 'GET'])
def friends():
	title = "My Friends List"

	if request.method == "POST":
		friend_name = request.form['name']
		new_friend = Friends(name=friend_name)

		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was an error adding your friend..."

	else:	
		friends = Friends.query.order_by(Friends.date_created)
		return render_template("friends.html", title=title, friends=friends)

@app.route('/')
def index():
	title = "Urja Mehta"
	return render_template("index.html", title=title)

@app.route('/about')
def about():
	title = "About Urja Mehta"
	return render_template("about.html", title=title)


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True) 