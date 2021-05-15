# https://towardsdatascience.com/web-app-development-in-python-469e1cf2116b
from flask import Flask, render_template

application = Flask(__name__)

first_name = 'Nicholas'
last_name = 'Kondal'

@application.route("/", methods=['GET'])
def home():
    return render_template('home.html', fn=first_name, ln=last_name)

application.run()