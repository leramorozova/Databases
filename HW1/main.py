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
        name = request.args['name']
        surname = request.args['surname']
        city = request.args['city']
        f_num = request.args['f_num']
        data.insert_user_info(name, surname, city, f_num)
        return redirect(url_for('success'))
    return render_template('add_info.html')


@app.route('/success/', methods=['POST', 'GET'])
def success():
    return render_template('success.html')


@app.route('/fail/', methods=['POST', 'GET'])
def fail():
    return render_template('fail.html')


@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.args:
        name = request.args['name']
        measure = request.args['measure']
        result = data.search(name, measure)
        if len(result) != 0:
            return render_template('result.html', result=result)
        else:
            return render_template('fail.html')
    return render_template('search.html')


@app.route('/view/', methods=['POST', 'GET'])
def view():
    info_kkal = data.viewer('kkal')
    info_kJ = data.viewer('kJ')
    return render_template('view.html', data_kkal=info_kkal, data_kJ=info_kJ)


if __name__ == '__main__':
    app.run(debug=True)
