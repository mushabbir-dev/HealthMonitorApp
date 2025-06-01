from flask import Flask, request, jsonify
from encrypt import encrypt_data, decrypt_data
from mongo_setup import save_encrypted_data, collection
from flask_cors import CORS
import time

AES_PASSWORD = "your-password-here"  # Set your decryption password

app = Flask(__name__)     # ✅ Initialize Flask app first
CORS(app)                 # ✅ THEN enable CORS

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        print("Received data:", data)

        start = time.time()
        encrypted = encrypt_data(str(data))
        encryption_time = time.time() - start

        print("Encrypted data:", encrypted)

        decrypted = decrypt_data(encrypted)
        print("Decrypted (for test):", decrypted)

        save_encrypted_data(encrypted)

        return jsonify({
            "status": "success",
            "message": "Data received and encrypted",
            "encrypted": encrypted,
            "encryption_time": round(encryption_time, 6)
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/decrypt', methods=['POST'])
def decrypt_route():
    try:
        req_data = request.get_json()
        encrypted = req_data.get('encrypted')
        password = req_data.get('password')

        if password != AES_PASSWORD:
            return jsonify({'status': 'error', 'message': 'Invalid password'}), 403

        start = time.time()
        decrypted_json = decrypt_data(encrypted)
        decryption_time = time.time() - start

        return jsonify({
            'status': 'success',
            'decrypted': decrypted_json,
            'decryption_time': round(decryption_time, 6)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/encrypted', methods=['GET'])
def get_encrypted_entries():
    try:
        data = list(collection.find().sort('_id', -1).limit(20))
        for doc in data:
            doc['_id'] = str(doc['_id'])
        return jsonify({'status': 'success', 'data': data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    from os import getenv
    port = int(getenv("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


