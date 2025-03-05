import flask

f = flask.Flask(__name__)


@f.route("/dodaj/<x>/<y>")
def dodaj(x, y):
    return {'result': float(x) + float(y)}


f.run(debug=True)
