from flask import Flask, request, jsonify, render_template_string
import instaloader
import re

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
        input[type="text"] { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { background-color: #E1306C; color: white; border: none; padding: 10px 15px; width: 100%; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #C13584; }
        #result { margin-top: 15px; font-weight: bold; color: #333; text-align: left; max-height: 200px; overflow-y: auto; font-size: 14px; background: #f9f9f9; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Comment Downloader</h1>
        <input type="text" id="postUrl" placeholder="Paste Instagram Post URL...">
        <button onclick="fetchComments()">Download Comments</button>
        <div id="result">इथे कमेंट्स दिसतील...</div>
    </div>

    <script>
        async function fetchComments() {
            const url = document.getElementById('postUrl').value;
            const resultDiv = document.getElementById('result');
            if(!url) {
                alert('कृपया इन्स्टाग्रामची वैध लिंक टाका!');
                return;
            }
            resultDiv.innerHTML = "इन्स्टाग्रामवरून कमेंट्स फेच करत आहे, कृपया थोडा वेळ वाट पहा...";
            
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                const data = await response.json();
                
                if(data.status === "success") {
                    let html = `<b>एकूण कमेंट्स: ${data.count}</b><br><br>`;
                    data.comments.forEach(c => {
                        html += `- <b>${c.author}</b>: ${c.text}<br>`;
                    });
                    resultDiv.innerHTML = html;
                } else {
                    resultDiv.innerHTML = "एरर: " + data.message;
                }
            } catch (err) {
                resultDiv.innerHTML = "काहीतरी तांत्रिक अडचण आली आहे.";
            }
        }
    </script>
</body>
</html>
"""

def extract_shortcode(url):
    match = re.search(r'/(?:p|reel)/([^/?#&]+)', url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    post_url = data.get('url')
    
    shortcode = extract_shortcode(post_url)
    if not shortcode:
        return jsonify({"status": "error", "message": "अवैध इन्स्टाग्राम पोस्ट लिंक!"})
    
    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        comments_list = []
        # सुरक्षिततेसाठी जास्तीत जास्त २० कमेंट्स फेच करूया
        count = 0
        for comment in post.get_comments():
            comments_list.append({"author": comment.owner.username, "text": comment.text})
            count += 1
            if count >= 20: 
                break
                
        return jsonify({
            "status": "success", 
            "count": len(comments_list),
            "comments": comments_list
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": "इन्स्टाग्राम सर्व्हरने रीतसर ब्लॉक केले किंवा पोस्ट खाजगी (Private) आहे."
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
