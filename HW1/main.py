import database as data
from flask import Flask
from flask import url_for, render_template, request, redirect

data.dataset_creator()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        return redirect(url_for('processing'))
    else:
        return render_template('form.html')


@app.route('/processing/', methods=['POST', 'GET'])
def proc():
    if request.args:
        name = request.args['name']
        proteins = request.args['proteins']
        fats = request.args['fats']
        carbs = request.args['carbs']
        data.insert_info(name, proteins, fats, carbs)
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