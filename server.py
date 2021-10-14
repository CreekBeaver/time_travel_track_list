from flask import Flask, request, jsonify
import os

# Configuration
app = Flask(__name__)

# Routes


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        print('Get Request Recieved')

        return "Response to a Get Request"
    if request.method == 'POST':
        print(request.get_json())
        #print(request.args)
        #copy_d = {}
        #for key in request.args:
        #    copy_d[key] = request.args[key]
        #print(copy_d)
        data = {'name' : 'Kyle Creek'}
        return jsonify(data)

# Listener


if __name__ == '__main__':
    app.run(port=9115, debug=True)