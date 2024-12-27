from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.blockchain import AadharVerificationSystem
from flask import request, current_app
from datetime import datetime
import math

main = Blueprint('main', __name__)
system = AadharVerificationSystem()

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/verify')
def verify():
    return render_template('verify.html')

@main.route('/history')
def history():
    return render_template('history.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/generate-otp', methods=['POST'])
def generate_otp():
    data = request.get_json()
    aadhar_number = data.get('aadhar_number')
    if not aadhar_number or len(aadhar_number) != 12:
        return jsonify({'success': False, 'error': 'Invalid Aadhaar number'})
    otp = system.generate_otp(aadhar_number)
    return jsonify({'success': True, 'otp': otp})

@main.route('/verify-transaction', methods=['POST'])
def verify_transaction():
    data = request.get_json()
    success = system.process_transaction(
        data.get('aadhar_number'),
        data.get('transaction_type'),
        data.get('otp')
    )
    if not success:
        if data.get('aadhar_number') not in system.otp_store:
            return jsonify({
                'success': False,
                'message': 'OTP expired. Please generate a new OTP'
            })
            
    return jsonify({
        'success': success,
        'message': 'Transaction verified and added to blockchain' if success else 'Verification failed'
    })

@main.route('/transaction-history/<aadhar_number>')
def transaction_history(aadhar_number):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'timestamp')
    sort_order = request.args.get('sort_order', 'desc')
    filter_type = request.args.get('filter_type', '')
    
    # Get all transactions for the Aadhar number
    all_transactions = system.get_transaction_history(aadhar_number)
    
    # Apply filtering
    if filter_type:
        all_transactions = [t for t in all_transactions if t['transaction_type'] == filter_type]
    
    # Apply sorting
    reverse = sort_order == 'desc'
    all_transactions.sort(
        key=lambda x: x[sort_by] if sort_by != 'timestamp' 
        else datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S.%f'),
        reverse=reverse
    )
    
    # Apply pagination
    total_items = len(all_transactions)
    total_pages = math.ceil(total_items / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    transactions = all_transactions[start_idx:end_idx]
    
    return jsonify({
        'transactions': transactions,
        'total_pages': total_pages,
        'current_page': page,
        'total_items': total_items
    })