
from flask import *
from flask_mysqldb import *
import mysql.connector

app=Flask(__name__)

app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']='rootmk'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_DB']= 'flaskdb'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql=MySQL(app)

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
    
        if request.form['pass1']==request.form['pass2']:
        
            fname=request.form['fname']#1
            #print('1')
            sname=request.form['sname']#2
            #print('2')
            gender=request.form.getlist('gender')#3
            #print(gender)
            #print('3')
            phone=request.form['phone']#4

            if len(phone)!=10:
                error='phone number is not valid'
                return render_template('register.html',error=error)

            #print('4')
            address=request.form['address']#5
            #print('5')
            tech=request.form.getlist('tech')#6
            #print('6')
            qulification=request.form.getlist('qulification')#7
            #print('7')
            email=request.form['email']#8
            username=request.form['userid']
            cur=mysql.connection.cursor()
            cur.execute('''SELECT * FROM register''')
            res=cur.fetchall()
            
            for i in res:

                if i['email']==email:
                    error='plse try diffrent email'
                    return render_template('register.html',error=error)

                if i['username']==username:
                    print(i['username'])
                    error='tyr different userid'
                    return render_template('register.html',error=error)
                
            #print('8')
            pas=request.form['pass1']#9
            #print('9')
        

            cur=mysql.connection.cursor()
            #cur.execute('''CREATE TABLE register (fistname VARCHAR(100), surname VARCHAR(100), gender VARCHAR(50), phonenumber INT, address VARCHAR(250), tech VARCHAR(50), qulification VARCHAR(50),email VARCHAR(100),username VARCHAR(100), password VARCHAR(100))''')
            cur.execute('''INSERT INTO register VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (fname,sname,gender,phone,address,tech,qulification,email,username,pas))
            print('hello5')
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('login'))
        else:
            error='re enter password is not correct'
            return render_template('register.html',error=error)
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        uname=request.form['username']
        pas=request.form['pas']
    


        cur=mysql.connection.cursor()
        cur.execute('''SELECT username FROM register''')
        re=cur.fetchall()

        error=None
        print(re)
        for i in re:
    
            if i['username']==uname:
    
        
                cur=mysql.connection.cursor()
                query='''SELECT password FROM register WHERE username='{0}' '''.format(uname)
                cur.execute(query)
                
                res=cur.fetchall()
                #print(res)
                #print(res[0])
        
                if res[0]['password']==pas:
                    #print('he')
            
                    
                    
                    # #qury='''SELECT * FROM demo1 where email='kittu@gmail.com' '''
                    qury='''SELECT * FROM register WHERE username='{0}' '''.format(uname)
                    print(qury)
                    cur.execute(qury)
                    resu=cur.fetchall()
                    print(resu)
                    rel=resu[0]
                    cur.close()
                    return render_template('profile.html',details=rel)
                else:
                    error='incorrect password'
                    return render_template('login.html',error=error)
        else:
            error='incorrect userid'
            return render_template('login.html',error=error)
        cur.close()




    return render_template('login.html')
if __name__=='__main__':
    app.run(debug=True)
