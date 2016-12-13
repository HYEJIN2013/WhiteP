from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb, utils

app = Flask(__name__)

app.secret_key = 'Zq4oA4Dqq3' 

currentUser = ''
loggedIn = False

@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    global loggedIn
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    queryType = 'None'
    if loggedIn == True:
      print('User: ' + session['username'])
      #print('Zipcode: ' + session['zipcode'])
    rows = []
    # if user typed in a post ...
    if request.method == 'POST':
      searchTerm = MySQLdb.escape_string(request.form['search'])
      if searchTerm == 'movies':         
         if loggedIn == True:
            query = "SELECT * from movies WHERE zip = '%s'" % session['zipcode']
            queryType = 'movies'
         else:
            query = "SELECT * from movies"
            queryType = 'movies'
      else:
        if loggedIn == True:
          query = "SELECT * FROM stores WHERE (name LIKE '%%%s%%' OR type LIKE '%%%s%%') AND (zip = '%s') ORDER BY name"  % (searchTerm, searchTerm, session['zipcode'])
          queryType = 'stores'
        else:
          query = "SELECT * FROM stores WHERE name LIKE '%%%s%%' OR type LIKE '%%%s%%' ORDER BY name" % (searchTerm, searchTerm)
          queryType = 'stores'
        print (query)
      cur.execute(query)
      rows = cur.fetchall()
      

    return render_template('index.html', queryType=queryType, results=rows, selectedMenu='Home', loggedIn=loggedIn)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global currentUser
    global loggedIn
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
      print "HI"
      username = MySQLdb.escape_string(request.form['username'])
      currentUser = username
      
      pw = MySQLdb.escape_string(request.form['pw'])
      query = "SELECT * from users WHERE username = '%s' AND password = SHA2('%s', 0)" % (username, pw)
      print query
      cur.execute(query)
           
      if cur.fetchone():
         session['username'] = currentUser         
         qy = "SELECT * from users WHERE username = '%s' AND password = SHA2('%s', 0)" % (username, pw)
         print qy
         cur.execute(qy)
         row = cur.fetchone()
         zipcode = row['zipcode']
         session['zipcode'] = zipcode
         q = "SELECT * from users WHERE username = '%s'" % session['username']
         print q
         cur.execute(q)          
         loggedIn=True
         return redirect(url_for('mainIndex'))
      else:
        print "mistake"
    return render_template('login.html', selectedMenu='Login', loggedIn=loggedIn)
 
  
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global currentUser
    global loggedIn
    session.pop('username', None)
    loggedIn=False
    return redirect(url_for('mainIndex'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    global currentUser
    global loggedIn
    db = utils.db_connect()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
      print "HI"
      username = MySQLdb.escape_string(request.form['username'])
      currentUser = username
      pw = MySQLdb.escape_string(request.form['pw'])
      zipcode = MySQLdb.escape_string(request.form['zipcode'])
      session['zipcode'] = zipcode 
      query = "INSERT INTO users (username, password, zipcode) VALUES ('%s', SHA2('%s', 0), '%s')" % (username, pw, session['zipcode'])
      print query
      cur.execute(query)
      
      session['username'] = currentUser         
      q = "SELECT * from users WHERE username = '%s'" % session['username']
      print q
      cur.execute(q)          
      loggedIn=True
      return redirect(url_for('mainIndex'))
      
    return render_template('register.html', selectedMenu='Register', loggedIn=loggedIn)
    
  

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=3000)
