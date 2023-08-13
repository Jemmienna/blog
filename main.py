from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

connection = psycopg2.connect(
                host='localhost',
                database='blog',
                user='postgres',
                password=''
            )

@app.route('/blog/add', methods=['GET'])
def blog_add():
    return render_template('add.html')

@app.route('/blog/add', methods=['POST'])
def blog_add_post():
    title = request.form.get('title')
    description = request.form.get('description')

    cursor=connection.cursor()
    cursor.execute("INSERT INTO \"blog_post\" (title, description) VALUES (%s, %s);", (title, description))
    connection.commit()
    cursor.close()

    if title and description:
        cursor = connection.cursor()
        select_query = "SELECT id FROM blog_post ORDER BY id desc limit 1"
        cursor.execute(select_query)
        blog_data = cursor.fetchall()
        cursor.close()
        return redirect('/blog/view?id=' + str(blog_data[0][0]))

    return redirect('/blog/add')

@app.route('/blog/', methods=['GET'])
def blog():
    cursor = connection.cursor()
    select_query = "SELECT id, title, description FROM blog_post"
    cursor.execute(select_query)
    blog_data = cursor.fetchall()
    cursor.close()

    return render_template('blog.html', blog_data=blog_data)

@app.route('/blog/view', methods=['GET'])
def view():
    id = request.args.get('id')
    
    if id == None:
        return redirect('/blog/')

    cursor = connection.cursor()
    select_query = f"select id, title, description from blog_post WHERE id={id} ORDER BY id desc;"
    cursor.execute(select_query)
    blog_data = cursor.fetchall()
    cursor.close()

    return render_template('view.html', blog_data=blog_data)

if __name__ == '__main__':
    app.run(debug=True)