from flask import Flask, request, render_template, jsonify, send_from_directory
from colorama import Fore, Style
import os
import socket
import qrcode

app = Flask(__name__)

# Folder tempat nyimpen file yang di-upload. Kalau belum ada, ya dibikin, bangsat.
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fungsi buat ngedeteksi IP lokal otomatis. Biar lo gak perlu ketik IP tiap kali, goblok.
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # Trik untuk ambil IP lokal
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

# QR generator: tampilkan di terminal + simpan sebagai file
def generate_qr():
    ip = get_local_ip()
    url = f"http://{ip}:5000"

    # Generate QR buat terminal
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)

    print(f"\n{Fore.GREEN}[INFO] Scan QR Code ini pake HP lo, tolol:\n")
    qr.print_ascii(invert=True)
    print(f"\n{Style.RESET_ALL}📲 {url}")

    # Simpen juga sebagai PNG, kalau lo butuh
    img = qr.make_image()
    img.save("qr_upload.png")
    print("[INFO] QR code juga disimpan di file 'qr_upload.png'")

# Tampilkan form upload dan list file yang udah di-upload.
@app.route('/')
def upload_form():
    file_list = os.listdir(UPLOAD_FOLDER)
    return render_template('upload.html', files=file_list)

# Tangani upload file dari HP/PC.
@app.route('/', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')
    saved_files = []

    for file in files:
        if file and file.filename:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            saved_files.append(file.filename)
            print(f"[UPLOAD] File '{file.filename}' berhasil diunggah.")

    return jsonify(saved_files)

# Ambil file yang udah di-upload.
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# Jalankan server dan tampilkan QR
if __name__ == '__main__':
    ip = get_local_ip()
    generate_qr()
    print(f"[SERVER] Jalan di: http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000)
