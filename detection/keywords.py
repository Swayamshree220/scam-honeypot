# Scam keyword database - expanded
SCAM_KEYWORDS = [
    # Prize/Lottery
    'won', 'prize', 'lottery', 'congratulations', 'winner', 'won rs',
    'claim', 'jackpot', 'lucky draw', 'selected', 'winning',
    
    # Banking/Account
    'account blocked', 'kyc', 'update details', 'verify account',
    'suspended', 'expire', 'reactivate', 'bank account', 'account number',
    'ifsc', 'ifsc code',
    
    # Payment
    'send money', 'transfer', 'pay now', 'processing fee',
    'charges', 'refundable', 'deposit', 'payment',
    'upi', '@paytm', '@phonepe', '@gpay', 'paytm', 'phonepe',
    
    # Urgency
    'urgent', 'immediate', 'immediately', 'hurry', 'last chance', 
    'expires today', 'act now', 'limited time', 'within 24 hours',
    
    # Links/Actions
    'click here', 'visit link', 'download app', 'install now',
    'call now', 'contact us', 'verify now',
    
    # Amounts
    'rs ', 'rupees', 'lakh', 'lakhs', 'crore', 'thousand',
    
    # Common scam phrases
    'confirm your', 'update your', 'verify your', 'claim your',
    'send your', 'provide your', 'share your'
]

SCAM_TYPES = {
    'lottery': ['won', 'prize', 'lottery', 'lucky', 'winning', 'claim'],
    'banking': ['account', 'kyc', 'bank', 'verify', 'blocked', 'suspended'],
    'payment_fraud': ['paytm', 'phonepe', 'gpay', 'upi', '@', 'send money', 'transfer'],
    'tech_support': ['virus', 'computer', 'technical', 'support', 'microsoft'],
    'romance': ['love', 'meet', 'lonely', 'dating', 'relationship'],
    'job': ['hiring', 'work from home', 'earn money', 'part time', 'job offer'],
    'phishing': ['click here', 'link', 'verify now', 'update now', 'expire'],
}