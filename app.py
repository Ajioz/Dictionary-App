from flask import Flask, render_template, url_for, request,flash, current_app
import mysql.connector
import datetime
import json
import os


app = Flask(__name__)

app.secret_key = 'secret'
mydb  = mysql.connector.connect(host = "127.0.0.1",
                               user = "root",
                               password = "Onoriode1!",
                               database = "dictionary",
                               auth_plugin = 'mysql_native_password')


@app.route('/', methods=['GET', 'POST'])
def index():
    user_response = ''
    if request.method == 'POST':
        user_input = request.form['word']
        if user_input == '':
            flash("We are not happy that you aren't following the rules. " 
                             "Kindly input words with meaning, don't leave it empty please!", "flash_error")    
        else:
            query = ("SELECT meaning FROM word WHERE word = %s")
            query_params = (user_input, )
            cursor = mydb.cursor(dictionary=True)
            cursor.execute(query, query_params)
            my_result  = cursor.fetchall()
            if (len(my_result) > 0):
                user_response = my_result[0]['meaning']
            else:
                user_response = ("Voila! I don't know this word, try adding it"
                                " at the dashboard or check back tomorrow.")
       
    return render_template('index.html', user_response = user_response)

@app.route('/dashboard')
def dashboard():
    cursor = mydb.cursor(dictionary=True)
    query = ('SELECT * FROM word')
    cursor.execute(query)
    my_result  = cursor.fetchall()
    for item in my_result:
        print(item)
    
    return render_template('dashboard.html', words = my_result)

@app.route('/word', methods=['POST'])
def add_word():
     req = request.get_json()
     word = req['word']
     meaning = req['meaning']
     if word =='' or meaning == '':
        flash("Something went wrong, Mmmm! We are as confused as you are. Ooops! You haven't inputed word with meaning", "flash_error")
     else:
        cursor = mydb.cursor(dictionary=True)
        query = "INSERT into word (word, meaning) VALUES (%s, %s)"
        val =  (word, meaning)
        cursor.execute(query, val)
        mydb.commit()
        cursor.close()
        flash("Word Successfully added!", "flash_success")
     
     return json.dumps('success')
 
@app.route('/word/<id>/delete', methods=['POST'])
def delete_word(id):
    word_id = id
    cursor = mydb.cursor(dictionary=True)
    query = "DELETE FROM word WHERE id = %s"
    val =  (word_id, )
    cursor.execute(query, val)
    mydb.commit()
    cursor.close()
    flash("Word Successfully deleted!", "flash_success")
     
    return json.dumps('success')

@app.route('/word/<id>/edit', methods=['POST'])
def edit_word(id):
    word_id = id
    req = request.get_json()
    word = req['word']
    meaning = req['meaning']
    if word =='' or meaning == '':
        flash("Gotcha! How about inputing word with meaning instead of leaving it empty", "flash_error")
    else:
        cursor = mydb.cursor(dictionary=True)
        query = "UPDATE word SET word = %s, meaning = %s WHERE id = %s"
        val =  (word, meaning, word_id)
        cursor.execute(query, val)
        mydb.commit()
        cursor.close()
        flash("Word Successfully updated!", "flash_success")
     
    return json.dumps('success')

@app.route('/add_logo', methods=['POST'])
def add_logo():
    image = request.files['file']
    
    if image :
        filepath = os.path.join(current_app.root_path, 'static/images/logo.png')
        image.save(filepath)
        flash('success')
    else:
        flash('Error!')   
          
    return 'Success!'
        
        
if __name__ =="__main__":
    app.run(debug=True)