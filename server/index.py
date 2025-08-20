# blockchain_app.py
import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from blockchain import Blockchain, Wallet

app = Flask(__name__)

blockchain = Blockchain()

users = [
    {'username': 'alice', 'password': 'Password$5', 'wallets' : [Wallet(), Wallet()]},
    {'username': 'Bob', 'password': 'Password$5', 'wallets' : [Wallet(), Wallet()]},
]

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    for user in users:
        if user['username'] == username:
            return jsonify({"error": "Username already exists."}), 409

    new_user = {
        'username': username,
        'password': password,
        'wallets': [Wallet()]
    }
    users.append(new_user)
    return jsonify({"message": "Account created successfully.", "user": new_user['username']}), 201

@app.route('/login', methods=['POST'])
def log_in():
    # Use form data instead of JSON
    username = request.form.get('username')
    password = request.form.get('password')

    for user in users:
        if user['username'] == username and user['password'] == password:
            return redirect(url_for("dashboard_page", username=username))

    return redirect(url_for("log_in_page"))

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required."}), 400

    for user in users:
        if user['username'] == username:
            user['wallets'].append(Wallet())
            return jsonify({"message": "Wallet created successfully.", "user": user['username']}), 201

    return jsonify({"error": "User not found."}), 404

@app.route('/get_balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    
    if not address:
        return jsonify({"error": "Wallet address is required."}), 400
    
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance}), 200

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    miner_address = data.get('miner_address')
    
    if not miner_address:
        return jsonify({"error": "Miner address is required."}), 400

    blockchain.mine(miner_address)
    return jsonify({"message": f"New block mined by {miner_address}."}), 200

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')
    signature = data.get('signature')

    if not all([sender, recipient, amount, signature]):
        return jsonify({"error": "Missing transaction data."}), 400

    blockchain.add_transaction(sender, recipient, amount, signature)
    return jsonify({"message": "Transaction added to pending pool."}), 201

@app.route('/get_wallets', methods=['GET'])
def get_wallets():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required."}), 400

    for user in users:
        if user['username'] == username:
            wallets = [{"address": wallet.address, "public_key": wallet.public_key.to_string().hex()} for wallet in user['wallets']]
            return jsonify({"username": username, "wallets": wallets}), 200

    return jsonify({"error": "User not found."}), 404

CLIENT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_client(path):
    if path == "":
        return send_from_directory(CLIENT_FOLDER, 'index.html')
    else:
        return send_from_directory(CLIENT_FOLDER, path)

# This is the new dashboard route
@app.route('/dashboard/<username>')
def dashboard_page(username):
    # This is where you would render your dashboard HTML template
    # For now, let's just return a simple message
    return f"Welcome to the dashboard, {username}!"

