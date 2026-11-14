from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solar Savings & Financing Estimator</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0px 8px 24px rgba(0,0,0,0.5); max-width: 480px; width: 100%; border: 1px solid #333; }
        h1 { color: #f39c12; font-size: 22px; text-align: center; margin-bottom: 5px; }
        .subtitle { font-size: 13px; color: #aaa; text-align: center; margin-bottom: 25px; }
        .card { background: #2a2a2a; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #3d3d3d; }
        label { font-size: 13px; color: #bbb; display: block; margin-bottom: 8px; }
        .value-display { font-size: 24px; font-weight: bold; color: #f39c12; margin-bottom: 10px; }
        input[type="range"] { width: 100%; accent-color: #f39c12; cursor: pointer; }
        input[type="number"] { width: 100%; padding: 10px; background: #121212; border: 1px solid #444; color: white; border-radius: 5px; box-sizing: border-box; font-size: 16px; margin-top: 5px; }
        #result { margin-top: 20px; background: #222; padding: 18px; border-radius: 8px; border: 1px solid #f39c12; display: none; }
        .result-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; border-bottom: 1px dashed #444; padding-bottom: 8px; }
        .whatsapp-btn { background-color: #25d366; margin-top: 15px; display: block; text-align: center; text-decoration: none; color: white; padding: 12px; border-radius: 5px; font-weight: bold; font-size: 15px; }
        .whatsapp-btn:hover { background-color: #1ebe5d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>☀️ SOLGURU STYLE ESTIMATOR</h1>
        <div class="subtitle">Calculate your savings. Plan your investment.</div>
        
        <div class="card">
            <label>Monthly Electricity Bill (₹)</label>
            <div class="value-display" id="billText">₹4,500</div>
            <input type="range" id="billRange" min="500" max="30000" step="500" value="4500" oninput="updateBillFromRange()">
            <input type="number" id="billInput" value="4500" oninput="updateBillFromInput()">
        </div>

        <div class="card">
            <label>Rate per Unit (₹)</label>
            <div class="value-display" id="rateText">₹8 / unit</div>
            <input type="range" id="rateRange" min="4" max="15" step="1" value="8" oninput="updateRate()">
        </div>
        
        <div id="result">
            <h3 style="margin:0 0 15px 0; color:#f39c12; font-size:16px; text-align:center;">📊 Estimated Summary</h3>
            <div class="result-row"><span>Recommended System:</span> <b id="resCapacity">-</b></div>
            <div class="result-row"><span>Estimated Total Cost:</span> <b id="resTotalCost">-</b></div>
            <div class="result-row"><span>PM Surya Ghar Subsidy:</span> <b style="color: #2ecc71;" id="resSubsidy">-</b></div>
            <div class="result-row"><span>Net Investment Cost:</span> <b id="resNetCost">-</b></div>
            <div class="result-row"><span>Monthly Savings:</span> <b style="color: #2ecc71;" id="resSavings">-</b></div>
            <div class="result-row"><span>Payback Period:</span> <b id="resPayback">-</b></div>
            
            <a id="whatsappLink" class="whatsapp-btn" target="_blank">📲 Connect via WhatsApp</a>
        </div>
    </div>

    <script>
        function updateBillFromRange() {
            let val = document.getElementById('billRange').value;
            document.getElementById('billInput').value = val;
            document.getElementById('billText').innerText = '₹' + Number(val).toLocaleString('en-IN');
            calculate();
        }

        function updateBillFromInput() {
            let val = document.getElementById('billInput').value;
            if(val) {
                document.getElementById('billRange').value = val;
                document.getElementById('billText').innerText = '₹' + Number(val).toLocaleString('en-IN');
                calculate();
            }
        }

        function updateRate
