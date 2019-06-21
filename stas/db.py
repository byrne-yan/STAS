#import sqlite3
from flask_pymongo import PyMongo

import click
from flask import current_app,g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
	if 'db' not in g:
		g.db = PyMongo(current_app).db
		# g.db = sqlite3.connect(
			# current_app.config['DATABASE'],
			# detect_types=sqlite3.PARSE_DECLTYPES
		# )
		# g.db.row_factory = sqlite3.Row
	return g.db
	
def close_db(e=None):
	db = g.pop('db',None)
	
	# if db is not None:
		# db.close()

def init_db():
	db = get_db()
	
	# with current_app.open_resource('schema.sql') as f:
		# db.executescript(f.read().decode('utf8'))
	
	db.users.drop()

def insert_user_into_db(username,password):
	if username is None or password is None:
		return 'username or password required'
	db = get_db()
	
	# if db.execute(
		# 'SELECT id FROM user WHERE username = ?', (username,)
		# ).fetchone() is not None:
		# return 'User "{}" is already registered.'.format(username)
	user = db.users.find_one({'user':username})
	if user is not None:
		return 'User "{}" is already registered.'.format(username)
			
	# db.execute(
		# 'INSERT INTO user (username, password) VALUES (?, ?)',
		# (username, generate_password_hash(password))
	# )
	# db.commit()
	
	db.users.insert_one({'user':username,'pwd':generate_password_hash(password)})
	
@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initialized the database.')

@click.command('add-user')
@click.option('--user')
@click.option('--pwd')
@with_appcontext
def add_user(user,pwd):
	error = insert_user_into_db(user,pwd)
	if error:
		click.echo(error)
	else:
		click.echo('User "{}" added.'.format(user))

@click.command('del-user')
@click.option('--user')
@with_appcontext
def del_user(user):
	db = get_db()
	# cursor = db.execute('DELETE from user WHERE username=?',(user,))
	res = db.users.remove({'user':user})
	print(res)
	if res['n'] > 0:
		click.echo('User "{}" Deleted.'.format(user))
		# db.commit()
	else:
		click.echo('Fail to delete user "{}"'.format(user))
		
@click.command('list-users')
@with_appcontext
def list_users():
	db = get_db()
	# cursor = db.execute('SELECT id, username FROM user')
	cursor = db.users.find({})
	for row in cursor:
		click.echo('{}'.format(row))
	
def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(add_user)
	app.cli.add_command(del_user)
	app.cli.add_command(list_users)
