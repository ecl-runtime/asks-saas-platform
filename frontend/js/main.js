const BACKEND_URL = "https://asks-backend.onrender.com";

document.getElementById('intentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const companyName = document.getElementById('companyName').value;
    const email = document.getElementById('email').value;
    const monthlySpend = document.getElementById('monthlySpend').value;
    
    const button = document.querySelector('.cta-button');
    button.disabled = true;
    button.textContent = 'Sending...';
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/intent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                company_name: companyName,
                email: email,
                monthly_spend: monthlySpend
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Request received. Our agent team will contact you within 2 hours.');
            document.getElementById('intentForm').reset();
            button.textContent = 'I need this guardrail';
            button.disabled = false;
        } else {
            alert('Error submitting request. Try again.');
            button.textContent = 'I need this guardrail';
            button.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Make sure backend is running.');
        button.textContent = 'I need this guardrail';
        button.disabled = false;
    }
});

console.log('ASKS frontend loaded. Backend URL:', BACKEND_URL);
