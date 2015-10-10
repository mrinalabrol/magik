from flask import flask, render_template, request, seesion, url_for

app = Flask(__name__)
account = {}

@app.route('/')
def main_site():
	return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	global account
	error = None
	if request.method == 'POST':
		if request.form['username'] not in account.keys() or request.form['password'] != account[request.form['username']]['password']:
			error = "Invalid Credentials. Please try again!"
		else:
			session['logged_in'] = True
			#flash('You were just logged in!')
			return redirect(url_for('page'))
	return render_template('login.html', error=error)

@app.route('/signup')
def signup():
	global account
	if request.method == 'POST':
		account[request.form['username']]['password']=request.form['password']
		account[request.form['username']]['name']=request.form['name']
		account[request.form['username']]['roll_no']=request.form['roll_no']
		account[request.form['username']]['electives']=request.form['electives']
		account[request.form['username']]['email']=request.form['email']
	return render_template('signup.html')

@app.route('/dash')
def page():
	return render_template('main_page.html')
