from flask import Flask,render_template
from searchpoet import searchpoet
from poetcount import poetcounts
from charanimal import charanimal
from charplant import charplant
from locword import locword
from wordsimilar import wordsimilar
from wordssentiment import wordssentiment
from Tangnet import Tangnet
app = Flask(__name__)
app.secret_key='123456'
urls=[searchpoet,poetcounts,charanimal,charplant,locword,wordsimilar,wordssentiment,Tangnet]
for url in urls:
    app.register_blueprint(url)

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
