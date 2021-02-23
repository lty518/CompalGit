from flask import Flask, request

app = Flask(__name__)
@app.route('/')
def index():
    return 'hello man'

@app.route('/register', methods=['POST'])
def Register():
    print("receive a register request")
    return 'Register POST Received!'

@app.route('/deregister', methods=['Get'])
def deregister():
    print("receive a deregister request")
    return 'Deregister POST Received!'

@app.route('/connection-status', methods=['POST'])
def GameConnection():
    print("receive a game connection post")
    dict = request.form
    print(dict)
    return 'GameConnection POST Received!'

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    dict = request.form
    print(dict)
    return '123'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
