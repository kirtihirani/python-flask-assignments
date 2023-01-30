from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"

db = SQLAlchemy(app)

class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    enroll = db.Column(db.String(200), nullable=False,primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.first_name}"


@app.route("/")

def hello_world():
    
    return render_template('index.html')
    # return 'hello world'

@app.route("/student",methods=['GET','POST'])
def student():
    print('hello')
    if request.method=='POST':
        enroll = request.form['enroll']
        first_name = request.form['firstname']        
        last_name = request.form['lastname']
        dob = request.form['dob']
        gender = request.form['gender']
        newstudent = Student(enroll=enroll,first_name=first_name,last_name=last_name,dob=dob,gender=gender)
        db.session.add(newstudent)
        db.session.commit()

    allstudent = Student.query.all()
    
    return render_template('student.html',allstudent=allstudent)

@app.route('/deleteStudent/<int:sno>')
def delete(sno):
    astudent = Student.query.filter_by(sno=sno).first()
    db.session.delete(astudent)
    db.session.commit()
    return redirect('/student')


@app.route("/updateStudent/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        enroll = request.form['enroll']
        first_name = request.form['firstname']        
        last_name = request.form['lastname']
        dob = request.form['dob']
        gender = request.form['gender']
        updated = Student.query.filter_by(sno=sno).first() 
        updated.enroll = enroll
        updated.first_name = first_name
        updated.last_name = last_name
        updated.dob = dob
        updated.gender = gender
        db.session.commit()
        return redirect("/student")
    stu = Student.query.filter_by(sno=sno).first()
    return render_template('updateStudent.html',stu=stu)


if __name__ == '__main__':
    app.run(debug=True)