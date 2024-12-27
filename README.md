# Decentralized_Aadhar_Verification
A blockchain-based solution for secure Aadhar-linked transactions
# Project Overview
This project implements a blockchain-based security system for Aadhaar transactions to enhance the security and immutability of Aadhaar-related data. The system provides a decentralized alternative to the current centralized database system, protecting against potential security breaches and unauthorized data modifications.
# Features
Decentralized storage of Aadhaar transaction data using blockchain technology
OTP-based verification system for Aadhaar transactions
Immutable transaction records
Web-based user interface for demonstration
Transaction validation and storage
Transparent transaction history viewing
# Technology Stack
Backend: Python
Blockchain Implementation: Custom blockchain using Python
Web Framework: Flask
Frontend: HTML, CSS, JavaScript
Authentication: OTP-based verification
# Installation
Clone the repository
Create and activate virtual environment:
python -m venv venv
source venv/bin/activate  # For Unix/MacOS
venv\Scripts\activate     # For Windows
# Usage
Start the Flask server: python run.py
Access the application:
Open your web browser
Navigate to http://localhost:8080
Follow the on-screen instructions to test the system
# How It Works
User Input: User enters their Aadhaar number through the web interface
OTP Generation: System generates a random OTP and simulates sending it to the registered phone number
Verification: User enters the OTP for verification
Blockchain Storage: Upon successful verification:
Transaction details are packaged into a block
Block is added to the blockchain
Transaction becomes immutable part of the chain
# Security Features
Decentralized data storage prevents single point of failure
Each block is cryptographically linked to previous blocks
Tampering with data requires modifying all subsequent blocks
OTP verification adds an additional layer of security
All transactions are timestamped and encrypted
# Disclaimer
This is a proof-of-concept implementation and should not be used in production without proper security auditing and enhancements. The system is designed to demonstrate the potential of blockchain technology in securing Aadhaar transactions.



