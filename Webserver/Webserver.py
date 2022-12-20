from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status.html')
def status():
    return render_template('status.html')

@app.route('/data.html')
def data():
    return render_template('data.html')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=5000)
