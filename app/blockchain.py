from datetime import datetime, timedelta
import hashlib
import random
import time
import re

class Block:
    def __init__(self, previous_hash, transaction_data):
        self.timestamp = datetime.now()
        self.transaction_data = transaction_data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = (
            str(self.timestamp) +
            str(self.transaction_data) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        
    def create_genesis_block(self):
        return Block("0", {"message": "Genesis Block"})

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, aadhar_number, transaction_type, verification_status):
        self.pending_transactions.append({
            "aadhar_number": aadhar_number,
            "transaction_type": transaction_type,
            "timestamp": str(datetime.now()),
            "verification_status": verification_status
        })

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return False
            
        new_block = Block(self.get_latest_block().hash, self.pending_transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return True

    def verify_chain_integrity(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

class AadharVerificationSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.otp_store = {}  # Temporary OTP storage
        
    def generate_otp(self, aadhar_number):
        """Generate a 6-digit OTP for the given Aadhar number"""
        otp = str(random.randint(100000, 999999))
        self.otp_store[aadhar_number] = (otp, datetime.now())
        return otp
    
    def verify_otp(self, aadhar_number, submitted_otp):
        """Verify the submitted OTP against stored OTP with expiration"""
        stored_data = self.otp_store.get(aadhar_number)
        if not stored_data:
            return False
            
        stored_otp, timestamp = stored_data
        current_time = datetime.now()
        
        if current_time - timestamp > timedelta(minutes=1):
            del self.otp_store[aadhar_number]
            return False
            
        return stored_otp == submitted_otp

    def process_transaction(self, aadhar_number, transaction_type, submitted_otp):
        """Process an Aadhar transaction with OTP verification"""
        if self.verify_otp(aadhar_number, submitted_otp):
            # Add verified transaction to blockchain
            self.blockchain.add_transaction(
                aadhar_number,
                transaction_type,
                "VERIFIED"
            )
            self.blockchain.mine_pending_transactions()
            # Clear OTP after successful verification
            del self.otp_store[aadhar_number]
            return True
        return False

    def get_transaction_history(self, aadhar_number):
        """Retrieve all transactions for a given Aadhar number"""
        transactions = []
        for block in self.blockchain.chain[1:]:  # Skip genesis block
            for transaction in block.transaction_data:
                if transaction.get("aadhar_number") == aadhar_number:
                    transactions.append(transaction)
        return transactions
    

def validate_aadhaar(aadhaar_number):
    # Remove all non-numeric characters using regular expressions
    cleaned_number = re.sub(r'[^0-9]', '', aadhaar_number)
    
    # Check if the cleaned Aadhaar number is exactly 12 digits and numeric
    if len(cleaned_number) != 12:
        raise ValueError("Invalid Aadhaar number! It must be exactly 12 digits without any special characters or spaces.")
    
    return cleaned_number

    
def main():
    while True:
        aadhaar_number = input("Enter your Aadhaar number: ").strip()  # Prompt the user for input and remove leading/trailing spaces
        try:
            # Validate the Aadhaar number
            validated_aadhaar = validate_aadhaar(aadhaar_number)
            print("Aadhaar number validated successfully:", validated_aadhaar)
            break  # Exit the loop after successful validation
        except ValueError as e:
            # Print the error and prompt the user again
            print(e)
            print("Please try again.")

if __name__ == "__main__":
    main()
