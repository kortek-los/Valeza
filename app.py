from flask import Flask, request, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

# Folder tempat nyimpen file yang di-upload. Kalau belum ada, ya dibikin, bangsat.
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route GET ke halaman utama, nampilin form upload dan list file yang udah ada. Simple banget, gak usah banyak bacot.
@app.route('/')
def upload_form():
    file_list = os.listdir(UPLOAD_FOLDER)  # Daftar file yang udah di-upload, biar keliatan di halaman
    return render_template('upload.html', files=file_list)

# Route POST ke '/' buat upload file. Jangan aneh-aneh, cuma ini jalannya.
@app.route('/', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')  # Ambil semua file dari inputan form
    saved_files = []

    for file in files:
        # Kalau filenya valid (ada nama dan gak kosong), langsung sikat simpen ke folder
        if file and file.filename:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)  # Simpen file. Udah gitu aja. Gampang, kan? Jangan bego.
            saved_files.append(file.filename)
            print(f"[UPLOAD] File '{file.filename}' berhasil diunggah.")  # Log ke console. Biar lo tau.

    # Balikin nama-nama file yang berhasil diupload. Biar bisa dicek dari frontend (atau postman kek).
    return jsonify(saved_files)

# Route GET buat ngambil file yang udah di-upload. Ya elah, masa upload bisa tapi download kagak.
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# Ini blok wajib. Jalankan aplikasinya di semua IP (0.0.0.0) dan port 5000.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
