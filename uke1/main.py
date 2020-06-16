from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hallo programmeringsklubben!'

@app.route('/hallo/<name>')
def hallo(name):
    return render_template('hallo.html', name = name)

@app.route('/info')
def info():
    return {
        'navn': 'Heidi',
        'favorittfarge': 'Lilla',
        'favorittspråk': 'Python'
    }

if __name__ == "__main__":
    app.run()

