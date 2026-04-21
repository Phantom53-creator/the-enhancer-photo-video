"""
The Enhancer - Photo & Video Enhancement Service
Main entrypoint with Stripe payment integration
"""

from flask import Flask, send_from_directory, render_template_string, request, jsonify
import stripe

app = Flask(__name__)

# Stripe configuration - TEST KEYS for development
stripe.api_key = 'sk_test_51QzfTIRhuKMH7b3GZ7mrdaMmvjBwCUgF4DJLSbbwT2rWHL6Znv8DRhTfVDM11PvV5RKQlDzgXYxiYuabAhTPiTWB00zt9Mwxni'
stripe_publishable_key = 'pk_test_51QzfTIRhuKMH7b3GR4Vbe0yTUadjEnflLqHzSAp7Ofn2LwXFYkUohxoFWA0VvJH2UMGLszAxYcLjnQMpOqN02f0U00aP3BPUmw'

# Route for main sales page
@app.route('/')
def home():
    """Main sales page"""
    return send_from_directory('.', 'salespage-v1.html')

# Route for variation 1
@app.route('/v1')
def v1():
    """Sales page variation 1"""
    return send_from_directory('.', 'salespage-v1.html')

# Route for variation 2
@app.route('/v2')
def v2():
    """Sales page variation 2"""
    return send_from_directory('.', 'salespage-v2.html')

# Route for variation 3
@app.route('/v3')
def v3():
    """Sales page variation 3"""
    return send_from_directory('.', 'salespage-v3.html')

# Stripe checkout page
@app.route('/checkout')
def checkout():
    """Stripe checkout page"""
    return render_template_string(CHECKOUT_HTML, stripe_publishable_key=stripe_publishable_key)

# Create payment intent
@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    """Create a Stripe PaymentIntent"""
    try:
        data = request.get_json()
        amount = data.get('amount', 2700)  # $27.00 in cents
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={'enabled': True}
        )
        
        return jsonify({
            'clientSecret': intent.client_secret,
            'publishableKey': stripe_publishable_key
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Payment success page
@app.route('/success')
def success():
    """Payment success page"""
    return render_template_string(SUCCESS_HTML)

# Payment cancel page
@app.route('/cancel')
def cancel():
    """Payment cancel page"""
    return render_template_string(CANCEL_HTML)

# API status endpoint
@app.route('/api/status')
def status():
    """API status endpoint"""
    return {
        "status": "operational",
        "service": "The Enhancer",
        "version": "1.0.0",
        "stripe_configured": bool(stripe.api_key),
        "pages_available": ["v1", "v2", "v3", "checkout", "success", "cancel"]
    }

# Checkout page HTML
CHECKOUT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout - The Enhancer</title>
    <script src="https://js.stripe.com/v3/"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .checkout-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .checkout-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .checkout-header h1 {
            color: #1f2937;
            font-size: 1.8rem;
            margin-bottom: 10px;
        }
        .checkout-header p {
            color: #6b7280;
        }
        .order-summary {
            background: #f9fafb;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .order-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .order-item:last-child {
            border-top: 2px solid #e5e7eb;
            padding-top: 10px;
            margin-top: 10px;
            font-weight: 700;
            font-size: 1.2rem;
        }
        #payment-form {
            margin-top: 20px;
        }
        #card-element {
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        #card-element.StripeElement--focus {
            border-color: #4f46e5;
        }
        #card-element.StripeElement--invalid {
            border-color: #dc2626;
        }
        .pay-button {
            width: 100%;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .pay-button:hover {
            transform: translateY(-2px);
        }
        .pay-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        #error-message {
            color: #dc2626;
            margin-top: 10px;
            font-size: 0.9rem;
        }
        .secure-badge {
            text-align: center;
            margin-top: 20px;
            color: #6b7280;
            font-size: 0.85rem;
        }
        .secure-badge span {
            color: #059669;
        }
    </style>
</head>
<body>
    <div class="checkout-container">
        <div class="checkout-header">
            <h1>Complete Your Order</h1>
            <p>The Enhancer - Professional AI Enhancement</p>
        </div>
        
        <div class="order-summary">
            <div class="order-item">
                <span>The Enhancer - Full Access</span>
                <span>$97.00</span>
            </div>
            <div class="order-item">
                <span>Founder Discount</span>
                <span style="color: #dc2626;">-$70.00</span>
            </div>
            <div class="order-item">
                <span>Total</span>
                <span style="color: #059669;">$27.00</span>
            </div>
        </div>
        
        <form id="payment-form">
            <div id="card-element"></div>
            <button type="submit" class="pay-button" id="submit-button">
                Pay $27.00
            </button>
            <div id="error-message"></div>
        </form>
        
        <div class="secure-badge">
            <span>🔒</span> Secured by Stripe. Your payment information is encrypted.
        </div>
    </div>

    <script>
        const stripe = Stripe('{{ stripe_publishable_key }}');
        const elements = stripe.elements();
        const cardElement = elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#1f2937',
                    '::placeholder': {
                        color: '#9ca3af'
                    }
                }
            }
        });
        cardElement.mount('#card-element');

        const form = document.getElementById('payment-form');
        const submitButton = document.getElementById('submit-button');
        const errorMessage = document.getElementById('error-message');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            submitButton.disabled = true;
            submitButton.textContent = 'Processing...';

            try {
                const response = await fetch('/create-payment-intent', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ amount: 2700 })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }

                const result = await stripe.confirmCardPayment(data.clientSecret, {
                    payment_method: {
                        card: cardElement
                    }
                });

                if (result.error) {
                    throw new Error(result.error.message);
                }

                window.location.href = '/success';
            } catch (error) {
                errorMessage.textContent = error.message;
                submitButton.disabled = false;
                submitButton.textContent = 'Pay $27.00';
            }
        });
    </script>
</body>
</html>
"""

# Success page HTML
SUCCESS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Successful - The Enhancer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .success-container {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        .success-icon {
            font-size: 5rem;
            margin-bottom: 20px;
        }
        h1 {
            color: #1f2937;
            font-size: 2rem;
            margin-bottom: 15px;
        }
        p {
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        .next-steps {
            background: #f0fdf4;
            border-radius: 12px;
            padding: 25px;
            margin: 30px 0;
            text-align: left;
        }
        .next-steps h3 {
            color: #059669;
            margin-bottom: 15px;
        }
        .next-steps ul {
            list-style: none;
            color: #374151;
        }
        .next-steps li {
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }
        .next-steps li::before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #059669;
            font-weight: 700;
        }
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 18px 40px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="success-icon">🎉</div>
        <h1>Payment Successful!</h1>
        <p>Welcome to The Enhancer! Your order has been confirmed and you're all set to start transforming your content.</p>
        
        <div class="next-steps">
            <h3>What's Next?</h3>
            <ul>
                <li>Check your email for access instructions</li>
                <li>Log in to your account dashboard</li>
                <li>Start uploading your images and videos</li>
                <li>Get professional 4K results in minutes</li>
            </ul>
        </div>
        
        <a href="/" class="cta-button">Go to Dashboard →</a>
    </div>
</body>
</html>
"""

# Cancel page HTML
CANCEL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Cancelled - The Enhancer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .cancel-container {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        .cancel-icon {
            font-size: 5rem;
            margin-bottom: 20px;
        }
        h1 {
            color: #1f2937;
            font-size: 2rem;
            margin-bottom: 15px;
        }
        p {
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 18px 40px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            margin: 10px;
        }
        .secondary-button {
            display: inline-block;
            background: #f3f4f6;
            color: #374151;
            padding: 18px 40px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="cancel-container">
        <div class="cancel-icon">😕</div>
        <h1>Payment Cancelled</h1>
        <p>No worries! Your payment was cancelled and no charges were made. You can try again whenever you're ready.</p>
        
        <a href="/checkout" class="cta-button">Try Again</a>
        <a href="/" class="secondary-button">Back to Home</a>
    </div>
</body>
</html>
"""

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Page Not Found - The Enhancer</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <p><a href="/">Go to Home</a></p>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)
