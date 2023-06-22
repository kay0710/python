'''
server for anyone
192.168.0.174:8081
'''

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main_page():
    return "This is the main page"

@app.route("/user", methods=['GET', 'POST'])
def post():
    if(request.method == 'GET'):
        return render_template('input.html')
    
    elif(request.method == 'POST'):
        value = request.form['input']
        return render_template('defalut.html', name=value)
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=8081)