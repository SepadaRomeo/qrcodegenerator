from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import qrcode

app = Flask(__name__)

# Create a directory for uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Generate the QR code linking to the uploaded image
            img_url = url_for('uploaded_file', filename=filename, _external=True)
            qr = qrcode.make(img_url)
            qr_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qr_code.png')
            qr.save(qr_file_path)

            return render_template('index.html', filename=filename, qr_code='qr_code.png')

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
