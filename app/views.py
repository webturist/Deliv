# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_jsglue import JSGlue     
from contextlib import closing 
import re 
from app.reserch import Coder
import app.pochta as pochta
import app.sat as sat
import app.deliv as deliv
import app.meest as meest

# create our little application :)
app = Flask(__name__)
JSGlue(app)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    if request.method == "POST":
        try:
            #print(request.get_json)
            d =dict(request.form)
            
            for data in d:
                d.update({data:d[data][0]})
            d["city_out"] = d["city_out"].split(", ")
            d["city_in"] = d["city_in"].split(", ")
            
            
            if d["cargoType"]=="TiresWheels":
                k={}
                for data in d:
                    if not re.search(Coder.tires, data):
                        k.update({data:d[data]})
                    elif d[data]:
                        k.update({data:d[data]})
                d=k
                del k                          
                
            print(d)
                
                        
            novapochta = pochta.cost(d)
            satcost = sat.cost(d)
            meestex = meest.cost(d)
            delcost = deliv.cost(d)
            
            print(novapochta)
            print(satcost)
            print(meestex)
            print(delcost)
            
            result = {"nova" :novapochta,"sat":satcost, "meest":meestex,"delivery":delcost}
                
                  
            return render_template('result.html', d=d,result=result)
        except:
            return  None        
    else:
        return render_template('show_entries.html', entries=entries)

@app.route("/search", methods=['GET'])
def search():
    """Search for places that match query."""
    if not request.args.get("q"):
        raise RuntimeError("missing q")
   
    q = request.args.get("q").capitalize() + "%"
       
    db = get_db() 
    temp = db.execute("""SELECT *
                            FROM ua
                            WHERE city LIKE ?
                            GROUP BY Region
                            LIMIT 20""", [q])    
    
    place =[]
    for row in temp.fetchall():
        d = {}
        for i in range(len(row)):
            d.update({row.keys()[i]:tuple(row)[i]})
        place.append(d)    
          
    return jsonify(place)
    
    

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/error')
def error():
    return render_template('404.html')
    


if __name__ == '__main__':
    init_db()