import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Tạo thư mục uploads nếu chưa tồn tại
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_aes_cipher(key, iv=None):
    # Tạo key 32 byte (AES-256) từ key người dùng nhập
    key_hash = hashlib.sha256(key.encode()).digest()
    if iv is None:
        iv = get_random_bytes(AES.block_size)
    return AES.new(key_hash, AES.MODE_CBC, iv), iv

def encrypt_file(input_file, output_file, key):
    cipher, iv = get_aes_cipher(key)
    
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(iv)
            while True:
                chunk = f_in.read(64 * 1024)  # 64KB chunks
                if len(chunk) == 0:
                    break
                elif len(chunk) % AES.block_size != 0:
                    chunk = pad(chunk, AES.block_size)
                f_out.write(cipher.encrypt(chunk))

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in:
        iv = f_in.read(AES.block_size)
        cipher, _ = get_aes_cipher(key, iv)
        
        with open(output_file, 'wb') as f_out:
            while True:
                chunk = f_in.read(64 * 1024)  # 64KB chunks
                if len(chunk) == 0:
                    break
                decrypted_chunk = cipher.decrypt(chunk)
                try:
                    decrypted_chunk = unpad(decrypted_chunk, AES.block_size)
                except ValueError:
                    pass  # Last chunk might not need padding
                f_out.write(decrypted_chunk)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        key = request.form.get('key', '')
        action = request.form.get('action', '')
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if not key:
            flash('Encryption/Decryption key is required')
            return redirect(request.url)
        
        # Lưu file tạm
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)
        
        # Tạo tên file output
        if action == 'encrypt':
            output_filename = f"encrypted_{file.filename}"
        else:
            if not file.filename.startswith('encrypted_'):
                flash('File to decrypt should start with "encrypted_"')
                return redirect(request.url)
            output_filename = f"decrypted_{file.filename[10:]}"
        
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        try:
            if action == 'encrypt':
                encrypt_file(input_path, output_path, key)
            else:
                decrypt_file(input_path, output_path, key)
            
            return redirect(url_for('download', filename=output_filename))
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(request.url)
        finally:
            # Xóa file input tạm
            if os.path.exists(input_path):
                os.remove(input_path)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)