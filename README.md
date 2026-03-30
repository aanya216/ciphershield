
# CipherShield 🔐

CipherShield is a web-based file encryption and decryption tool built using Flask and Python.  
It allows users to securely encrypt and decrypt files using a password-based dynamic key system combined with bitwise transformations.

The application provides a clean web interface where users can upload files, set a password, choose bitwise shift parameters, and download encrypted or decrypted outputs.

---

## Features

• File encryption and decryption  
• Password-based dynamic key generation  
• Bitwise circular shift operations  
• XOR-based byte transformation  
• Interactive web interface  
• Drag-and-drop file upload  
• Progress feedback during processing  

---

## Encryption Algorithm

CipherShield processes files **byte-by-byte** using a multi-step transformation pipeline.

### 1. Password Key Generation
The password characters are XORed together to generate a base key.

### 2. Dynamic Key Scheduling
For each byte in the file, a dynamic key is generated using:

dynamic_key = (base_key + index × 7) mod 256

This ensures different bytes use different keys.

### 3. Byte Transformation
Each byte undergoes three operations:

1. Circular left bit shift  
2. XOR with the dynamic key  
3. Circular right bit shift  

### 4. Decryption
Decryption reverses these operations in the opposite order to recover the original file.

This approach ensures that identical bytes at different positions produce different encrypted outputs.

---

## Technologies Used

- Python
- Flask
- HTML / CSS
- JavaScript
- Bitwise Operations

---

## Project Structure
CipherShield/
│
├── app.py
├── requirements.txt
│
├── templates/
│ └── index.html
│
└── README.md


---

## Installation

Clone the repository:

bash
git clone https://github.com/aanya216/ciphershield.git
cd ciphershield

---

Install Dependencies:
pip install -r requirements.txt

---

Run the Application: 
python app.py

---

The application will start on:
http://127.0.0.1:5000

---

# How to use

1. Open the web interface
2. Upload a file
3. Enter a password
4. Select encryption or decryption
5. Choose the shift bit configuration
6. Run the process
7. Download the processed file

---

# Security Note

CipherShield is designed as an educational project demonstrating encryption concepts such as XOR operations, dynamic keys, and bitwise shifts.

It should not be used for protecting highly sensitive or production data.

--- 

# Example Workflow

For Encryption: 
Original File + Select Shift Bits + Enter Password = Encrypted File

For Decryption:
Encrypted File + Original Password + Selected Shift Bits = Original File

---

# Future Improvements

• Stronger cryptographic key derivation
• AES-based encryption option
• File integrity verification
• Drag-and-drop multiple files
• Docker deployment

---

# Author

Aanyaa Patel

---

# License

This project is licensed under the MIT License.

---

# Topics used in the Project

- XOR encryption
- Circular bit shifts
- Dynamic keys
- Flask routes
- File handling

---

# Demo

Application Interface:
![Interface](ss/interface.png)

Encryption Result:
![Interface](ss/encryption.png)

Decrption Result:
![Interface](ss/decryption.png)

---
