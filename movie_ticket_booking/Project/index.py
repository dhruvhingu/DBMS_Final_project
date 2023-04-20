from flask import Flask, render_template, request, redirect, url_for, session
import re
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
app = Flask(__name__,template_folder="templates")
app.secret_key = ' key'
app.static_folder='static'
x=[]
@app.route("/")
def first():
    return render_template('first.html')
@app.route("/login/", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    # session={}
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
        con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
        
        cursor = con.cursor()
        cursor.execute('SELECT * FROM form WHERE username = :username AND password = :password',{"username": username, "password": password})
        account = cursor.fetchone()
        #print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account[2]
            session['username'] = account[0]
            global x
            x=[]
            x.append(account[0])
            x.append(account[2])
            x.append(account[3])
            # Redirect to home page
            if 'loggedin' in session:
        # User is loggedin show them the home page
                return redirect(url_for('home'))
    # User is not loggedin redirect to login page
            return redirect(url_for('login'))
        else:
        # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template("login.html",msg=msg)
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    print("hi")
    try:
        msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'dob' in request.form:
        # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            d = request.form['dob']
            
            print(d)
            aa=d.split("-")
            month={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JULY",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
            dob=aa[2]+'-'+month[int(aa[1])]+'-'+aa[0]
            print(dob)
        # Check if account exists using MySQL
            cursor = con.cursor()
            # cursor.execute('SELECT * FROM form WHERE username = :username OR email = :email',{"username": username,"email":email})
            # account = cursor.fetchone()
        # If account exists show error and validation checks
            
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            # elif not re.match(r'[A-Za-z0-9]+', username):
            #     msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email or not dob:
                msg = 'Please fill out the form!'
            else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.callproc('insert_data_proc', [username,password,email,dob])
                con.commit()
                con.close()
                msg = 'You have successfully registered!'
        elif request.method == 'POST':
        # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
    # Show registration form with message (if any)
        return render_template('register.html', msg=msg)
    
    except Exception as e:
        return render_template('error.html',message=str(e))

@app.route('/add_shows',methods=['GET','POST'])
def add_shows():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor=con.cursor()
    cursor.execute('SELECT * from cinema ')
    result2 = cursor.fetchall()
    cursor.execute('SELECT * from movies ')
    result1 = cursor.fetchall()
    try:
        if 'movie_id' in request.form and 'cinema_id' in request.form and 'show_time' in request.form and 'show_date' in request.form:
            print('hi')
            movie_id = request.form['movie_id']
            cinema_id = request.form['cinema_id']
            show_time = request.form['show_time']
            show_date = request.form['show_date']
            aa=show_date.split("-")
            month={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JULY",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
            show_date=aa[2]+'-'+month[int(aa[1])]+'-'+aa[0]
            print(show_date)
            cursor.execute('insert into shows values (DEFAULT,:cinema_id,:movie_id,:show_date,:show_time,DEFAULT)',{'cinema_id':cinema_id,'movie_id':movie_id,'show_date':show_date,'show_time':show_time})
            print('dataentered')
            con.commit()
            cursor.close()
            con.close()
    except Exception as e:
        return render_template('error.html',message=str(e))
    return render_template('add_shows.html',r1=result1,r2=result2)

@app.route('/error')  
def error(message):
    return render_template('error.html',message=message)
@app.route('/home/')
def home():
    print(x)
    return render_template("home.html")
def getMovies(search):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    search = search.lower()
    cursor.execute("Select * from movies where lower(title) like :search or genre like :search",('%'+search+'%','%'+search+'%'))
    results = cursor.fetchall()
    print(results)
    con.close()
    return results

@app.route("/search/", methods=['GET', 'POST'])
def search_result():
    col = ["Movie id:   ","Title:   ","Movie Description:   ","Duration:   ","Language:   ","Release Date:   ","Genre:   "]
    if request.method=="POST":
        data = request.form['search']
        print(data)
        users = getMovies(data)
        print(users)
    else:
        users = []
    return render_template("search.html",usr=users)
def filter(data1,data2,data3=None):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    datax=""
    for i in data1:
        if(i==data1[0] ):
            if (len(data1)>1):
                datax="'"+i+"'"+","
            else:
                datax="'"+data1[0]+"'"
        elif(i==data1[-1]):
            datax=datax+"'"+i+"'"
        else:
            datax=datax+"'"+i+"'"+","
    print(datax)
    datay = ""
    for i in data2:
        if(i==data2[0] ):
            if (len(data2)>1):
                datay="'"+i+"'"+","
            else:
                datay="'"+data2[0]+"'"
        elif(i==data2[-1]):
            datay=datay+"'"+i+"'"
        else:
            datay=datay+"'"+i+"'"+","
    query = "SELECT * FROM movies WHERE "
    if datax:
        query += "genre IN ( " +datax +')'
        
    if datay:
        if data1:
            query +=' AND '
        query += "lower(lang) IN ('" + "','".join(data2) + "')"


        print(data2)
        
    if data3:
        if datax or datay:
            query += " AND "
        available_time = "SELECT movie_id  FROM shows WHERE show_time = '"+ data3 +"'"
        query += "movie_id IN ( " + available_time + ")"
    print("This is the query here:",query)
    cursor.execute(query)
    results = cursor.fetchall()
    con.close()
    return results

@app.route("/filter/",methods=['GET','POST'])
def filter_result():
    if 'time' in request.form:
        data3 = request.form['time']
        print(data3)
    else:
        data3 = None
    if request.method=="POST":
        data1,data2 = request.form.getlist('mycheckbox'),request.form.getlist('mycheckbox1')
        # print(data1,data2)
        users = filter(data1,data2,data3)
    else:
        users = []
    return render_template("search.html",usr=users)


def cinema(data):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    cursor.execute('select cinema_id from shows where movie_id = :data' ,(data,))
    results = cursor.fetchall()
    print(results)
    result=[]
    for i in results:
        cursor.execute('select city from cinema where cinema_id in :results',(i))
        res= cursor.fetchone()
        result.append(res)
    con.close()
    result=set(result)
    print(result)
    return result
@app.route("/cinema/",methods=['GET','POST'])
def select_cinema():
    data= request.args.get('data')
    print(data)
    
    if(data.isdigit()):
        data1=cinema(data)
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
        con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
        cursor = con.cursor()
        cursor.execute('select title from movies where movie_id = :data',{'data':data})
        data2=cursor.fetchone()
        session['movie'] = data2[0]
        return render_template('cinema.html',dt=data1,dt2=data)
    else:
        session['movie'] = data
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
        con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
        cursor = con.cursor()
        cursor.execute('select movie_id from movies where title = :title',{'title':data})
        dx = cursor.fetchone()
        print(dx[0])
        data1 = cinema(dx[0])
        return render_template('cinema.html',dt=data1,dt2=dx[0])

@app.route("/image/")
def image_result():
    image_id = request.args.get('data')
    print(image_id)
    print(type(image_id))
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM movies WHERE title LIKE :image_id", ('%'+image_id+'%',))
    result = cursor.fetchall()
    print(result)
    return render_template("search.html",usr=result)
@app.route("/shows/",methods = ['GET','POST'])
def shows():
    city=request.form['mycity']
    city=city.split(",")
    print(city[0])
    print(city[1])
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)

    cursor=con.cursor()
    query = """
        SELECT DISTINCT s.show_time, c.cinema_name, to_char(s.show_date,'DD-MM-YYYY'),s.available_seats,m.price ,s.show_id
        FROM cinema c
        JOIN shows s ON s.cinema_id = c.cinema_id
        JOIN movies m ON m.movie_id = s.movie_id
        WHERE c.city = :city AND m.movie_id = :movie_id
    """
    cursor.execute(query, {'city': city[0], 'movie_id': city[1]})
    result = cursor.fetchall()
    print(result)
    session['show_time']=result[0][0]
    session['cinema_name']=result[0][1]
    session['show_date']=result[0][2]
    session['price']=result[0][4]
    session['show_id']=result[0][5]
    return render_template('shows.html',ct=result)

    
@app.route("/seats/")
def seats():
    return render_template("seats.html")

@app.route("/reserve/",methods=['GET','POST'])
def reserve():
    seat_list = request.form.get('seats_input')
    showid= request.args.get('showid')
    print(seat_list)
    user_id=session['id']
    seat_list=seat_list[2:]
    seat_list=seat_list[:-2]
    seats=list(map(int,seat_list.split('","')))
    print(showid)
    seats2=str(seats)
    print(str(seats))
    print(len(seats))
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor=con.cursor()
    cursor.execute('insert into tickets values(DEFAULT,:user_id,:show_id,:seat_id)',{'user_id':user_id,'show_id':showid,'seat_id':seats2})
    price=session.get('price')
    con.commit()
    cursor.close()
    con.close()
    session['no_of_tickets']=len(seats)
    session['price2']=len(seats)*session.get(price)
    return render_template("reserve.html",seats=seats,no_of_seats=len(seats),price=price)

@app.route("/theater/")
def city():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor=con.cursor()
    cursor.execute('Select distinct city from cinema')
    d = cursor.fetchall()
    return render_template("city.html",dt=d)

@app.route("/movies/",methods=['GET','POST'])
def movies():
    # if request.form =="POST":
    city = request.form['mycity']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    cursor=con.cursor()
    cursor.execute('select cinema_name from cinema where city = :city',{'city':city})
    c = cursor.fetchall()
    return render_template("theater.html",ct=c)
    # else:
    #     return 'method not allowed'
@app.route("/schedule/" ,methods = ['GET','POST'])
def schedule():
    data = request.args.get('data')
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    print(data)
    cinema_name=data
    cursor=con.cursor()
    query = """
        SELECT DISTINCT s.show_time, m.title, to_char(s.show_date,'DD-MM-YYYY'),s.available_seats,S.SHOW_ID,m.price,c.cinema_name, s.show_id
           FROM movies m
           JOIN shows s ON s.movie_id = m.movie_id
           JOIN cinema c on c.cinema_id = s.cinema_id
           WHERE c.cinema_name = :cname
    """
    cursor.execute(query, {'cname':data})
    result = cursor.fetchall()
    # print(cinema_name,"xyz")
    session['show_time']=result[0][0]
    session['movie']=result[0][1]
    session['show_date']=result[0][2]
    session['price']=result[0][5]
    session['cinema_name']=result[0][6]
    session['show_id']=result[0][7]
    con.commit()
    cursor.close()
    print(result)
    return render_template('movie-schedule.html',ct=result)

@app.route("/payment/",methods = ['GET','POST'])
def payment():
    seat_list = request.form.get('seats_input')
    showid= session.get('show_id')
    print(seat_list)
    user_id=session['id']
    seat_list=seat_list[2:]
    seat_list=seat_list[:-2]
    seats=list(map(int,seat_list.split('","')))
    print(showid)
    seats2=str(seats)
    print(len(seats))
    
    session['no_of_tickets']=len(seats)
    session['price2']=len(seats)*session.get('price')
    return render_template('payment.html')


@app.route("/success/",methods = ['GET','POST'])
def success():
    det = list()
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
    con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
    payment_method='Net Banking'
    status='Paid'
    cursor=con.cursor()
    cursor.execute('insert into Payment values(DEFAULT,:payment_method,:status)',{'payment_method':payment_method,'status':status})
  
    username = session.get('username')
    user_id=session.get('id')
    title = session.get('movie')
    date = session.get('show_date')
    time = session.get('show_time')
    price2 = session.get('price2')
    show_id=session.get('show_id')
    no_of_tickets = session.get('no_of_tickets')
    print(no_of_tickets,"asda")
    each_price =session.get('price')
    cinema_name =session.get('cinema_name')
    print(price2)
    print(username)

    cursor.execute('insert into tickets values (DEFAULT,:username,:show_id,:price)',{'username':user_id,'show_id':show_id,'price':price2})
    
    det.append(username)
    det.append(title)
    det.append(time)
    det.append(date)
    det.append(cinema_name)
    det.append(each_price)
    det.append(no_of_tickets)
    det.append(price2)
    return render_template('success.html',details = det)

@app.route('/user/',methods=['GET','POST'])
def profile():
    if 'username' in request.form and 'email' in request.form and 'password' in request.form:
        print('hi')
        nuser = request.form['username']
        nemail = request.form['email']
        npass = request.form['password']
        cdsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl') 
        con = cx_Oracle.connect(user='daps', password="daps", dsn=dsn_tns)
        cursor = con.cursor()
        cursor.execute('update form set username = :nuser, email = :nemail, password = :npass where username = :x',{'nuser':nuser,'nemail':nemail,'npass':npass,'x':x[0]}) # use the x variable in the SQL query
        con.commit() # commit the changes to the database
        cursor.close()
        con.close()
        return render_template('user.html', usr=[nuser, nemail]) # render the user.html template with the updated user information
    else:
        print('hello')
        print(x)
        return render_template('user.html',usr=x)

app.debug = True
app.run()