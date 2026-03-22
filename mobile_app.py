from flask import Flask, request, jsonify, render_template_string
import base64, os, json
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
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #f0f8e8;
            max-width: 480px;
            margin: 0 auto;
            padding: 15px;
        }
        h1 {
            text-align: center;
            color: #2E7D32;
            margin: 15px 0;
            font-size: 24px;
        }
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            font-size: 17px;
            cursor: pointer;
            margin: 8px 0;
            font-weight: bold;
        }
        .btn-green  { background:#4CAF50; color:white; }
        .btn-blue   { background:#2196F3; color:white; }
        .btn-orange { background:#FF9800; color:white; }
        .preview img {
            width: 100%;
            border-radius: 12px;
            margin: 10px 0;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card h3 { color:#2E7D32; margin-bottom:8px; }
        .card p  { color:#333; line-height:1.6; }
        .loading {
            text-align:center;
            padding:20px;
            color:#666;
            font-size:18px;
        }
        .error { color:red; padding:10px; }
        .ingredient-tag {
            display:inline-block;
            background:#E8F5E9;
            color:#2E7D32;
            padding:5px 10px;
            border-radius:20px;
            margin:3px;
            font-size:14px;
        }
        .recipe-item {
            border-left:4px solid #4CAF50;
            padding:8px 12px;
            margin:8px 0;
            background:#f9f9f9;
            border-radius:0 8px 8px 0;
        }
        .calorie-big {
            font-size:36px;
            font-weight:bold;
            color:#FF5722;
            text-align:center;
        }
        .nutrition-row {
            display:flex;
            justify-content:space-between;
            padding:5px 0;
            border-bottom:1px solid #eee;
        }
    </style>
</head>
<body>

<h1>🍳 AI Smart Kitchen</h1>

<input type="file" id="fileInput"
       accept="image/*" capture="environment"
       style="display:none" onchange="handleFile(this)">

<button class="btn btn-green"
        onclick="document.getElementById('fileInput').click()">
    📷 Take Photo / Upload Image
</button>

<div class="preview" id="preview"></div>

<button class="btn btn-orange" id="scanBtn"
        onclick="scanFood()" style="display:none">
    🔍 Scan Ingredients
</button>

<div id="results"></div>

<script>
let imgData = null;

function handleFile(input) {
    if (!input.files || !input.files[0]) return;
    const reader = new FileReader();
    reader.onload = e => {
        imgData = e.target.result;
        document.getElementById('preview').innerHTML =
            '<img src="' + imgData + '">';
        document.getElementById('scanBtn').style.display = 'block';
        document.getElementById('results').innerHTML = '';
    };
    reader.readAsDataURL(input.files[0]);
}

function speak(text) {
    try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-US';
        u.rate = 0.85;
        u.pitch = 1;
        u.volume = 1;
        window.speechSynthesis.speak(u);
    } catch(e) {
        console.log('Speech error:', e);
    }
}

async function scanFood() {
    if (!imgData) {
        alert('Please select an image first!');
        return;
    }

    document.getElementById('results').innerHTML =
        '<div class="loading">⏳ AI Scanning... Please wait</div>';
    document.getElementById('scanBtn').disabled = true;

    speak("Scanning your food. Please wait.");

    try {
        const res = await fetch('/scan', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({image: imgData})
        });

        const data = await res.json();
        showResults(data);

    } catch(err) {
        document.getElementById('results').innerHTML =
            '<div class="card error">❌ Error: ' + err + 
            '<br>Please check internet connection!</div>';
        speak("Error scanning. Please try again.");
    }

    document.getElementById('scanBtn').disabled = false;
}

function showResults(data) {
    let html = '';

    // Ingredients
    html += '<div class="card">';
    html += '<h3>🥕 Detected Ingredients</h3>';
    if (data.ingredients && data.ingredients.length > 0) {
        data.ingredients.forEach(i => {
            html += '<span class="ingredient-tag">' + i + '</span>';
        });
        speak("I detected " + data.ingredients.length + 
              " items. They are " + data.ingredients.join(', ') + ".");
    } else {
        html += '<p>No food items detected. Try another photo!</p>';
        speak("No food detected. Please try another photo.");
    }
    html += '</div>';

    // Calories
    html += '<div class="card">';
    html += '<h3>🔥 Calories</h3>';
    html += '<div class="calorie-big">' + 
            (data.total_calories || 0) + ' kcal</div>';
    if (data.nutrition && data.nutrition.length > 0) {
        data.nutrition.forEach(n => {
            html += '<div class="nutrition-row">';
            html += '<span>' + n.name + '</span>';
            html += '<span>' + n.calories + ' kcal | ';
            html += 'P:' + n.protein_g + 'g | ';
            html += 'C:' + n.carbs_g + 'g | ';
            html += 'F:' + n.fat_g + 'g</span>';
            html += '</div>';
        });
    }
    html += '</div>';

    // Recipes
    html += '<div class="card">';
    html += '<h3>🍽️ Recipe Suggestions</h3>';
    if (data.recipes && data.recipes.length > 0) {
        data.recipes.forEach(r => {
            html += '<div class="recipe-item">';
            html += '<b>📌 ' + r.title + '</b>';
            html += '<p>' + r.instructions + '</p>';
            if (r.missing && r.missing.length > 0) {
                html += '<p style="color:red">❌ Missing: ' + 
                        r.missing.join(', ') + '</p>';
            } else {
                html += '<p style="color:green">✅ Ready to cook!</p>';
            }
            html += '</div>';
        });
        speak("I found " + data.recipes.length + 
              " recipes. Top recipe is " + data.recipes[0].title);
    } else {
        html += '<p>No recipes found for these items.</p>';
    }
    html += '</div>';

    // Shopping List
    if (data.shopping && data.shopping.length > 0) {
        html += '<div class="card">';
        html += '<h3>🛒 Shopping List</h3>';
        data.shopping.forEach(s => {
            html += '<div class="nutrition-row">';
            html += '<span>' + s.priority + ' ' + s.item + '</span>';
            html += '<span>Qty: ' + s.qty + '</span>';
            html += '</div>';
        });
        html += '</div>';
    }

    document.getElementById('results').innerHTML = html;
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "No image",
                          "ingredients": [],
                          "nutrition": [],
                          "total_calories": 0,
                          "recipes": [],
                          "shopping": []})

        # Save image
        image_str = data['image']
        if ',' in image_str:
            image_str = image_str.split(',')[1]

        img_bytes = base64.b64decode(image_str)
        img = Image.open(io.BytesIO(img_bytes))
        img = img.convert('RGB')
        img.save("scan.jpg", quality=85)

        # Detect
        from kitchen_detection import detect_ingredients
        from nutrition import get_nutrition
        from recipe_suggester import suggest_recipes

        ingredients = detect_ingredients("scan.jpg")
        nutrition, total = get_nutrition(ingredients)
        recipes = suggest_recipes(ingredients)

        # Shopping list
        shopping = []
        try:
            from shopping_list import generate_shopping_list
            shopping = generate_shopping_list(ingredients)
        except:
            pass

        return jsonify({
            "ingredients":    ingredients,
            "nutrition":      nutrition,
            "total_calories": total,
            "recipes":        recipes,
            "shopping":       shopping,
            "status":         "success"
        })

    except Exception as e:
        print(f"Scan error: {e}")
        return jsonify({
            "error":          str(e),
            "ingredients":    [],
            "nutrition":      [],
            "total_calories": 0,
            "recipes":        [],
            "shopping":       [],
            "status":         "error"
        }), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    print(f"🍳 AI Smart Kitchen starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)