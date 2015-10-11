from flask import Flask, render_template, request, session, url_for, redirect
import time
from functools import wraps

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session.keys():
			return f(*args, **kwargs)
		else:
			return redirect(url_for('main_site'))
	return wrap

app = Flask(__name__)
account = {}
#minute = time.strftime("%M")

app.secret_key = "kaala kaluta"

@app.route('/')
def main_site():
	return render_template('index.html')

@app.route('/login.html', methods = ['GET', 'POST'])
def login():
	global account
	error = None
	if request.method == 'POST':
		if request.form['username'] not in account.keys() or request.form['password'] != account[request.form['username']]['password']:
			error = "Invalid Credentials. Please try again!"
		else:
			session['logged_in'] = True
			session['username'] = request.form['username']
			month = time.strftime("%b")
			day = int(time.strftime("%d"))
			if(month == 'Oct'):
				account[session['username']]['week'] = ((3 + day)/7) + 9
			elif(month == 'Nov'):
				account[session['username']]['week'] = ((34 + day)/7) + 9
			elif(month == 'Dec'):
				account[session['username']]['week'] = ((64 + day)/7) + 9
			elif(month == 'Jan'):
				account[session['username']]['week'] = ((95 + day)/7) + 9
			elif(month == 'Feb'):
				account[session['username']]['week'] = ((126 + day)/7) + 9
			elif(month == 'Mar'):
				account[session['username']]['week'] = ((154 + day)/7) + 9
				#flash('You were just logged in!')
				#minute = time.strftime("%M")
			account[session['username']]['day'] = time.strftime("%a")	
			return redirect(url_for('page'))
	return render_template('login.html', error=error)

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
	global account
	if request.method == 'POST':
		account[request.form['username']] = {'username1':request.form['username'], 'password':request.form['password'], 'name':request.form['name'], 'roll_no':request.form['roll_no'], 'electives':request.form['elective'], 'email':request.form['email']}
		account[request.form['username']]['group'] = int(account[request.form['username']]['roll_no'][4:])%6
		
		#else:
		#	account[request.form['username']]['week'] = ((3 + day)/7) + 9
		print (account)
		return redirect(url_for('main_site'))
		#account[request.form['username']]['name']=request.form['name']
		#account[request.form['username']]['roll_no']=request.form['roll_no']
		#account[request.form['username']]['electives']=request.form['electives']
		#account[request.form['username']]['email']=request.form['email']
		print (account)
	return render_template('signup.html')

@login_required
@app.route('/main')
def page():
	global account
	return render_template('mainpage.html', week=account[session['username']]['week'], day=account[session['username']]['day'], USER=account[session['username']]['username1'], ROLL=account[session['username']]['roll_no'])

@login_required
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('main_site'))
	
if __name__ == '__main__':
	app.run(debug=True, port=8080)
