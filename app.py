"""
File Encryption and Decryption Tool
Author: Aanyaa Patel

This project implements a simple encryption and decryption algorithm
using XOR operations and circular bit shifts on file bytes.
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max

# -------------------------------
# BITWISE OPERATIONS
# -------------------------------

def left_circular_shift(byte, n):
    return ((byte << n) | (byte >> (8 - n))) & 0xFF

def right_circular_shift(byte, n):
    return ((byte >> n) | (byte << (8 - n))) & 0xFF

# -------------------------------
# KEY GENERATION
# -------------------------------

def generate_base_key(password):
    key = 0
    for ch in password:
        key ^= ord(ch)
    return key

def get_dynamic_key(base_key, index):
    return (base_key + index * 7) % 256

# -------------------------------
# ENCRYPTION / DECRYPTION
# shift: left-shift amount for encrypt (1-4 bits)
# The right-shift on encrypt = shift // 2 (min 1), reversed on decrypt
# -------------------------------

def encrypt_byte(byte, key, shift):
    rshift = max(1, shift // 2)
    byte = left_circular_shift(byte, shift)
    byte ^= key
    byte = right_circular_shift(byte, rshift)
    return byte

def decrypt_byte(byte, key, shift):
    rshift = max(1, shift // 2)
    byte = left_circular_shift(byte, rshift)
    byte ^= key
    byte = right_circular_shift(byte, shift)
    return byte

def process_file(data, password, mode, shift=3):
    base_key = generate_base_key(password)
    result = bytearray()
    fn = encrypt_byte if mode == 'encrypt' else decrypt_byte
    for i, byte in enumerate(data):
        key = get_dynamic_key(base_key, i)
        result.append(fn(byte, key, shift))
    return bytes(result)

# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    password = request.form.get('password', '')
    mode = request.form.get('mode', 'encrypt')
    shift = int(request.form.get('shift', 3))

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    if mode not in ('encrypt', 'decrypt'):
        return jsonify({'error': 'Invalid mode'}), 400
    if shift not in (1, 2, 3, 4):
        return jsonify({'error': 'Invalid shift value'}), 400

    try:
        data = file.read()
        result = process_file(data, password, mode, shift)

        original_name = secure_filename(file.filename)
        if mode == 'encrypt':
            out_name = original_name + '.enc'
        else:
            out_name = original_name.removesuffix('.enc') if original_name.endswith('.enc') else 'decrypted_' + original_name

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(out_name)[1])
        tmp.write(result)
        tmp.close()

        response = send_file(tmp.name, as_attachment=True, download_name=out_name)

        @response.call_on_close
        def cleanup():
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)