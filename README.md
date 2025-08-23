# Project Overview

This is a simple, full-stack web application built with Python and Flask that simulates a basic cryptocurrency wallet system. Users can view their wallets, check balances, mine new blocks, and send transactions. The application uses a mock blockchain to handle transactions and balances, providing a hands-on demonstration of key blockchain concepts.

<img width="400" alt="image" src="https://github.com/user-attachments/assets/31e08291-0650-465f-885c-16b11acf37e4" />


## ✨ Features

* **User Authentication**: A login page allows users to access their personalized wallet dashboards.
* **Wallet Dashboard**: Displays a user's unique wallets, each with a clickable link to view its details. The balances automatically refresh every second.
* **Dynamic Wallet Pages**: Each wallet has its own page showing its address and current balance.
* **Mining Functionality**: Users can "mine" a new block to receive a reward, with real-time feedback and an updated balance.
* **Transaction System**: A pop-up menu allows users to send money from their wallet to a recipient address.

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### Installation & Running the Application

To set up and run the application, follow these steps:

1.  Clone the repository and navigate to your project directory:
    ```bash
    git clone https://github.com/AlanMet/Full-Stack-Crypto.git
    cd Full-Stack-Crypto
    ```

2.  Navigate into the server directory:
    ```bash
    cd server/
    ```

3.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # On macOS and Linux
    venv\Scripts\activate    # On Windows
    ```

4.  Install the required packages, including Flask:
    ```bash
    pip install Flask
    ```

5.  Set the `FLASK_APP` environment variable and run the application:
    ```bash
    export FLASK_APP=index.py
    flask run
    ```
## 🖥️ Usage
<img width="400" alt="Wallets dashboard" src="https://github.com/user-attachments/assets/3b7aefef-4796-4c51-a32a-06e2d265b709" />
<img width="400" alt="image" src="https://github.com/user-attachments/assets/80ea231a-0301-4d82-a9ff-0c20b6b6ecf7" />

1. **Home Page**: Navigate to the home page to see the landing page. Click "Log In" to proceed.
*URL: `/`*

2. **Login**: Use one of the following mock user credentials to log in:

* **username**: `alice`, **password**: `Password$5`

* **username**: `Bob`, **password**: `Password$5`
  *URL: `/login`*

3. **Wallets Dashboard**: You will be redirected to your personal wallet page, showing a list of your wallets.
*URL: `/wallets/<username>`*

4. **Wallet Details**: Click on a wallet to view its address and current balance.
*URL: `/wallets/<username>/<address>`*

5. **Mine a Block**: Click the "Mine" button to start the mining process. A pop-up will provide feedback and automatically update your balance once the block is mined.

6. **Send a Transaction**: Click the "Send Money" button to open a form where you can enter a recipient's address and an amount to send.

## 🧑‍💻 Contributing

This project is a personal demonstration, but feel free to fork the repository, make improvements, and submit a pull request.

1. Fork the project.

2. Create your feature branch (`git checkout -b feature/NewFeature`).

3. Commit your changes (`git commit -m 'Add some NewFeature'`).

4. Push to the branch (`git push origin feature/NewFeature`).

5. Open a Pull Request.

## 📄 License

Distributed under the MIT License.
