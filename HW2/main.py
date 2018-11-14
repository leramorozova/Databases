import db_backend as data
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def form():
    return render_template('form.html')


@app.route('/add_user/', methods=['POST', 'GET'])
def add_user():
    if request.args:
        user_name = request.args['name']
        user_surname = request.args['surname']
        user_city = request.args['city']
        user_age = request.args['user_age']
        data.insert_user_info(user_name, user_surname, user_city, user_age)
        if request.args['f_name']:
            f_name = request.args['f_name']
            f_surname = request.args['f_surname']
            f_city = request.args['f_city']
            f_age = request.args['f_age']
            data.insert_friend_info(user_name, user_surname, user_city, user_age,
                                    f_name, f_surname, f_city, f_age)
        return redirect(url_for('success'))
    return render_template('add_user.html')


@app.route('/success/', methods=['POST', 'GET'])
def success():
    return render_template('success.html')


@app.route('/fail/', methods=['POST', 'GET'])
def fail():
    return render_template('fail.html')


@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.args:
        parameter = request.args['parameter']
        value = request.args['value']
        result = data.search(parameter, value)
        if len(result) != 0:
            return render_template('result.html', result=result)
        else:
            return render_template('fail.html')
    return render_template('search.html')


@app.route('/view_registered/', methods=['POST', 'GET'])
def view_registered():
    users = data.view_registered()
    return render_template('view_registered.html', users=users)


@app.route('/view_all/', methods=['POST', 'GET'])
def view_all():
    users = data.view_all()
    return render_template('view_all.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
