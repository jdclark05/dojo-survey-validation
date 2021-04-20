from flask import Flask,render_template,redirect,request,session,flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)
app.secret_key = "validation"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.form:
        is_valid = True
        if len(request.form['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters!")
        try :
            dojo_id = int(request.form['dojo_id']) 
        except Exception:
            is_valid = False
            flash("Must select Dojo!")
        try :
            language_id = int(request.form['language_id']) 
        except Exception:
            is_valid = False
            flash("Must select Language!")
        if len(request.form['comment']) < 3:
            is_valid = False
            flash("Comment must be at least 3 characters!")
        if not is_valid:
            return redirect('/')
        else:
            query = "INSERT INTO students (name, comment, dojo_id, language_id) VALUES (%(name)s, %(comment)s, %(dojo_id)s, %(language_id)s);"
            data = {
                "name":request.form['name'],
                "comment":request.form['comment'],
                "dojo_id":request.form['dojo_id'],
                "language_id":request.form['language_id']
            }
            student_id = connectToMySQL('dojo-survey').query_db(query, data)
            return redirect(f"/display/{student_id}")
    else:
        query_dojos = "SELECT * FROM dojos;"
        query_languages = "SELECT * FROM languages;"
        dojos = connectToMySQL('dojo-survey').query_db(query_dojos)
        languages = connectToMySQL('dojo-survey').query_db(query_languages)
        return render_template("index.html", dojos=dojos, languages=languages)


@app.route('/display/<int:student_id>', methods=["GET"])
def display(student_id):
        query = "SELECT students.name, dojos.location, languages.language, students.comment FROM students JOIN languages on languages.id = students.language_id JOIN dojos on dojos.id = students.dojo_id WHERE students.id = %(student_id)s;"
        data = {
            "student_id":student_id
        }
        students = connectToMySQL('dojo-survey').query_db(query, data)
        print(students)
        return render_template("display.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)