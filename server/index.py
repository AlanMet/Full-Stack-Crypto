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
    username = request.form.get('username')
    password = request.form.get('password')

    for user in users:
        if user['username'] == username and user['password'] == password:
            return redirect(url_for("wallets_page", username=username))

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

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/login')
def log_in_page():
    return render_template('login.html')

@app.route('/wallets/<string:username>')
def wallets_page(username):
    user_wallets = []
    for user in users:
        if user['username'] == username:
            user_wallets = user['wallets']
            break
            
    wallets_with_balance = []
    for wallet in user_wallets:
        balance = blockchain.get_balance(wallet.address)
        wallets_with_balance.append({'address': wallet.address, 'balance': balance})
            
    return render_template('wallets.html', username=username, wallets=wallets_with_balance)

@app.route('/wallets/<string:username>/<string:address>')
def wallet_page(username, address):
    is_valid_wallet = False
    for user in users:
        if user['username'] == username:
            for wallet in user['wallets']:
                if wallet.address == address:
                    is_valid_wallet = True
                    break
            break

    if not is_valid_wallet:
        return redirect(url_for('wallets_page', username=username))

    balance = blockchain.get_balance(address)
    return render_template('wallet.html', username=username, address=address, balance=balance)
