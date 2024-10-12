from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pyngrok import ngrok

# Wprowadź swój authtoken tutaj
ngrok.set_auth_token("2jHir8X6llX1wdW6zGaIiPE2aWR_28jTfysAvbrm4t1RrbQ4G")

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('draw_line')
def handle_draw(data):
    emit('draw_line', data, broadcast=True)

if __name__ == '__main__':
    # Utworzenie tunelu ngrok
    public_url = ngrok.connect(5000)
    print(f'Public URL: {public_url}')
    
    # Uruchom serwer Flask na porcie 5000
    socketio.run(app, port=5000)
