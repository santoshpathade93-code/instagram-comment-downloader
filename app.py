from flask import Flask, request, jsonify, render_template_string, Response

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Comment Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: center; max-width: 450px; width: 100%; }
        h1 { color: #333; font-size: 22px; margin-bottom: 15px; }
        input[type="text"], textarea { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; font-family: Arial, sans-serif; }
        textarea { resize: vertical; height: 100px; }
        button { background-color: #E1306C; color: white; border: none; padding: 10px 15px; width: 100%; border-radius: 5px; font-size: 16px; cursor: pointer; margin-bottom: 10px; }
        button:hover { background-color: #C13584; }
        .download-btn { background-color: #2e7d32; }
        .download-btn:hover { background-color: #1b5e20; }
        #result { margin-top: 15px; font-weight: bold; color: #333; text-align: left; max-height: 200px; overflow-y: auto; font-size: 14px; background: #f9f9f9; padding: 10px; border-radius: 5px; }
        .info { font-size: 13px; color: #666; margin-bottom: 15px; text-align: left; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Comment Downloader</h1>
        <div class="info">टीप: इन्स्टाग्रामच्या सिक्युरिटीमुळे थेट लिंक चालत नाही, म्हणून खाली तुम्ही कमेंट्स पेस्ट करून त्यांची फाईल बनवू शकता.</div>
        
        <input type="text" id="postUrl" placeholder="Paste Instagram Post URL...">
        <textarea id="commentsInput" placeholder="कमेंट्स इथे पेस्ट करा (प्रत्येक ओळीत एक कमेंट)..."></textarea>
        
        <button onclick="processComments()">Process Comments</button>
        <button class="download-btn" onclick="downloadFile()">Download as TXT File</button>
        
        <div id="result">इथे प्रक्रिया केलेल्या कमेंट्स दिसतील...</div>
    </div>

    <script>
        let savedComments = "";

        function processComments() {
            const commentsText = document.getElementById('commentsInput').value;
            const resultDiv = document.getElementById('result');
            
            if(!commentsText.trim()) {
                alert('कृपया काहीतरी कमेंट्स पेस्ट करा!');
                return;
            }

            savedComments = commentsText;
            const lines = commentsText.split('\\n').filter(line => line.trim() !== '');
            
            let html = `<b>एकूण कमेंट्स: ${lines.length}</b><br><br>`;
            lines.forEach((c, index) => {
                html += `${index + 1}. ${c}<br>`;
            });
            resultDiv.innerHTML = html;
        }

        async function downloadFile() {
            if(!savedComments.trim()) {
                alert('डाऊनलोड करण्यासाठी पहिले कमेंट्स प्रोसेस करा!');
                return;
            }

            const response = await fetch('/download-txt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comments: savedComments })
            });
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'instagram_comments.txt';
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download-txt', methods=['POST'])
def download_txt():
    data = request.get_json()
    comments = data.get('comments', '')
    
    return Response(
        comments,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=instagram_comments.txt"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
