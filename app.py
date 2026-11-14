from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Subsidy & Savings Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; padding: 25px; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); max-width: 450px; width: 100%; }
        h1 { color: #2e7d32; font-size: 20px; text-align: center; margin-bottom: 5px; }
        .subtitle { font-size: 13px; color: #666; text-align: center; margin-bottom: 20px; }
        label { font-weight: bold; font-size: 14px; color: #333; display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; font-size: 16px; }
        button { background-color: #2e7d32; color: white; border: none; padding: 12px; width: 100%; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #1b5e20; }
        #result { margin-top: 20px; background: #e8f5e9; padding: 15px; border-radius: 8px; display: none; font-size: 14px; color: #2e7d32; line-height: 1.6; }
        .whatsapp-btn { background-color: #25d366; margin-top: 15px; display: block; text-align: center; text-decoration: none; color: white; padding: 12px; border-radius: 5px; font-weight: bold; font-size: 15px; }
        .whatsapp-btn:hover { background-color: #1ebe5d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>☀️ सोलर सबसिडी व बचत कॅल्क्युलेटर</h1>
        <div class="subtitle">तुमचे विजेचे बिल टाका आणि तապसा किती सबसिडी मिळेल!</div>
        
        <label>महिन्याचे सरासरी वीज बिल (₹):</label>
        <input type="number" id="billAmount" placeholder="उदा. 2500">
        
        <button onclick="calculateSolar()">कॅल्क्युलेट करा</button>
        
        <div id="result">
            <h3 style="margin:0 0 10px 0; color:#1b5e20; font-size:16px;">अंदाजे हिशोब:</h3>
            <div id="resCapacity"></div>
            <div id="resSubsidy"></div>
            <div id="resSavings"></div>
            <a id="whatsappLink" class="whatsapp-btn" target="_blank">📲 थेट व्हॉट्सॲपवर कोटेशन मागवा</a>
        </div>
    </div>

    <script>
        function calculateSolar() {
            const bill = parseFloat(document.getElementById('billAmount').value);
            if(!bill || bill <= 0) {
                alert('कृपया वैध वीज बिल रक्कम टाka!');
                return;
            }

            let units = bill / 8;
            let kw = Math.ceil(units / 120); 
            if(kw < 1) kw = 1;
            if(kw > 10) kw = 10;

            let subsidy = 0;
            if(kw == 1) subsidy = 30000;
            else if(kw == 2) subsidy = 60000;
            else if(kw >= 3) subsidy = 78000;

            let monthlySavings = bill * 0.85;

            document.getElementById('resCapacity').innerHTML = `<b>शिफारस केलेले सोलर युनिट:</b> ${kw} kW`;
            document.getElementById('resSubsidy').innerHTML = `<b>सरकारी अंदाजे सबसिडी:</b> ₹${subsidy.toLocaleString('en-IN')}`;
            document.getElementById('resSavings').innerHTML = `<b>दरमहा अंदाजे बचत:</b> ₹${Math.round(monthlySavings).toLocaleString('en-IN')}`;
            
            // तुमचा व्हॉट्सॲप नंबर 9226127472 जोडलेला आहे
            let phone = "919226127472"; 
            let msg = `नमस्कार, मला माझ्या घरी ${kw} kW चा सोलर बसवायचा आहे. वीज बिल सुमारे ₹${bill} येते. मला अधिक माहिती हवी आहे.`;
            document.getElementById('whatsappLink').href = `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`;
            
            document.getElementById('result').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
