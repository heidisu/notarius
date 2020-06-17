from flask import Flask, render_template, request, redirect
from notat import get_notater, add_notat

app = Flask(__name__)

@app.route('/')
def notater():
    notater = get_notater()
    return render_template('index.html', notater = notater)

@app.route('/notat', methods=('GET', 'POST'))
def nytt_notat():
    if request.method == 'POST':
        tittel = request.form['tittel']
        tekst = request.form['tekst']
        add_notat(tittel, tekst)
        return redirect('/')

    return render_template('nytt_notat.html')

if __name__ == "__main__":
    app.run() #port='8000', host='127.0.0.1')
