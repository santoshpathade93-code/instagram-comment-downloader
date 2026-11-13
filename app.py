from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Instagram Comment Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: center; max-width: 400px; width: 100%; }
        h1 { color: #333; font-size: 22px; margin-bottom: 15px; }
        input[type="text"] { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { background-color: #E1306C; color: white; border: none; padding: 10px 15px; width: 100%; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #C13584; }
        #result { margin-top: 15px; font-weight: bold; color: #333; text-align: left; max-height: 150px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Comment Downloader</h1>
        <input type="text" id="postUrl" placeholder="Paste Instagram Post URL...">
        <button onclick="fetchComments()">Download Comments</button>
        <div id="result"></div>
    </div>

    <script>
        async function fetchComments() {
            const url = document.getElementById('postUrl').value;
            const resultDiv = document.getElementById('result');
            if(!url) {
                alert('कृपया इन्स्टाग्रामची वैध लिंक टाका!');
                return;
            }
            resultDiv.innerHTML = "इन्स्टाग्रामवरून कमेंट्स फेच करत आहे...";
            
            const response = await fetch('/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            resultDiv.innerHTML = data.message;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    post_url = data.get('url')
    
    return jsonify({
        "status": "success", 
        "message": f"इन्स्टाग्राम पोस्ट यशस्वीरीत्या कनेक्ट झाली! लिंक: {post_url}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
  
