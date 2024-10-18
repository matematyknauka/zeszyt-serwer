from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
from pyngrok import ngrok
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# Wprowadź swój authtoken tutaj
ngrok.set_auth_token("wprowadz-token")

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('draw_line')
def handle_draw(data):
    emit('draw_line', data, broadcast=True)

@app.route('/save', methods=['POST'])
def save_drawing():
    drawing_data = request.json.get('drawing_data', [])
    
    # Tworzenie tymczasowego pliku PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
        c = canvas.Canvas(tmpfile.name, pagesize=letter)
        
        # Rozmiar strony PDF
        pdf_width, pdf_height = letter
        
        # Ustawienie grubości linii na większą wartość
        c.setLineWidth(3)  # Ustawienie grubości linii na 3

        # Rysowanie na PDF
        for line in drawing_data:
            x0 = line['x0']
            y0 = pdf_height - line['y0']  # Odwrócenie Y
            x1 = line['x1']
            y1 = pdf_height - line['y1']  # Odwrócenie Y
            
            c.line(x0, y0, x1, y1)  # Rysowanie linii w PDF
        
        c.save()
        
        return send_file(tmpfile.name, as_attachment=True, download_name="drawing.pdf")

if __name__ == '__main__':
    # Utworzenie tunelu ngrok
    public_url = ngrok.connect(5000)
    print(f'Public URL: {public_url}')
    
    # Uruchom serwer Flask na porcie 5000
    socketio.run(app, port=5000)
