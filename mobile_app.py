from flask import Flask, request, jsonify, render_template_string
import base64, os
from PIL import Image
import io

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Smart Kitchen</title>
    <style>
        body {
            font-family: Arial;
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            background: #f0f8e8;
        }
        h1  { color: #2d6a2d; text-align: center; font-size: 24px; }
        .btn {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            width: 100%;
            margin: 8px 0;
            cursor: pointer;
        }
        .btn:hover { background: #45a049; }
        .card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        img { max-width: 100%; border-radius: 10px; }
        .loading { text-align:center; color:#666; }
    </style>
</head>
<body>
    <h1>🍳 AI Smart Kitchen</h1>

    <input type="file" id="camera"
           accept="image/*" capture="environment"
           style="display:none"
           onchange="previewImage(this)">

    <button class="btn"
            onclick="document.getElementById('camera').click()">
        📷 Take Photo / Upload
    </button>

    <div id="preview"></div>

    <button class="btn" id="scanBtn"
            onclick="scanImage()"
            style="display:none; background:#2196F3;">
        🔍 Scan Ingredients
    </button>

    <div id="results"></div>

    <script>
    let imageData = null;

    function previewImage(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = e => {
                imageData = e.target.result;
                document.getElementById('preview').innerHTML =
                    '<img src="' + imageData + '">';
                document.getElementById('scanBtn').style.display = 'block';
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    async function scanImage() {
        document.getElementById('results').innerHTML =
            '<p class="loading">⏳ Scanning... please wait</p>';

        const response = await fetch('/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({image: imageData})
        });

        const data = await response.json();

        let html = '';

        html += '<div class="card">';
        html += '<h3>🥕 Ingredients:</h3>';
        html += '<p>' + (data.ingredients.join(', ') || 'None detected') + '</p>';
        html += '</div>';

        html += '<div class="card">';
        html += '<h3>🔥 Calories:</h3>';
        html += '<p>' + data.total_calories + ' kcal total</p>';
        data.nutrition.forEach(n => {
            html += '<p>• ' + n.name + ': ' + n.calories + ' kcal</p>';
        });
        html += '</div>';

        html += '<div class="card">';
        html += '<h3>🍽️ Recipes:</h3>';
        if (data.recipes.length > 0) {
            data.recipes.forEach(r => {
                html += '<p>📌 <b>' + r.title + '</b></p>';
                html += '<p>' + r.instructions + '</p>';
            });
        } else {
            html += '<p>No recipes found</p>';
        }
        html += '</div>';

        html += '<div class="card">';
        html += '<h3>🛒 Shopping Needed:</h3>';
        if (data.shopping.length > 0) {
            data.shopping.forEach(s => {
                html += '<p>' + s.priority + ' ' + s.item + '</p>';
            });
        } else {
            html += '<p>✅ All stocked!</p>';
        }
        html += '</div>';

        document.getElementById('results').innerHTML = html;
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data       = request.json
        image_data = data['image'].split(',')[1]
        img_bytes  = base64.b64decode(image_data)
        img        = Image.open(io.BytesIO(img_bytes))
        img.save("mobile_scan.jpg")

        from kitchen_detection import detect_ingredients
        from nutrition         import get_nutrition
        from recipe_suggester  import suggest_recipes
        from shopping_list     import generate_shopping_list

        ingredients        = detect_ingredients("mobile_scan.jpg")
        nutrition, total   = get_nutrition(ingredients)
        recipes            = suggest_recipes(ingredients)
        shopping           = generate_shopping_list(ingredients)

        return jsonify({
            "ingredients":   ingredients,
            "nutrition":     nutrition,
            "total_calories": total,
            "recipes":       recipes,
            "shopping":      shopping
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("📱 Mobile App Starting...")
    print("Open your phone browser and go to:")
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print(f"👉 http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)