from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Replace these with your actual Edamam API ID and key
EDAMAM_API_ID = '111111'
EDAMAM_API_KEY = '111111111111'
EDAMAM_API_URL = 'https://api.edamam.com/search'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recipe Finder</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            color: #333;
            background-color: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
        }
        input[type="text"], button {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            box-shadow: inset 0 1px 3px 0 rgba(0,0,0,0.1);
        }
        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border: none;
        }
        button:hover {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Recipe Finder</h2>
        <form method="POST">
            <input type="text" name="query" placeholder="Search for a recipe...">
            <button type="submit">Search</button>
        </form>
        {% if recipes %}
            <div>
                <h3>Results:</h3>
                <ul>
                    {% for recipe in recipes %}
                        <li><a href="{{ recipe.url }}">{{ recipe.label }}</a></li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def recipe_finder():
    recipes = []
    if request.method == 'POST':
        query = request.form['query']
        params = {
            'q': query,
            'app_id': EDAMAM_API_ID,
            'app_key': EDAMAM_API_KEY
        }
        response = requests.get(EDAMAM_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            recipes = [{'label': recipe['recipe']['label'], 'url': recipe['recipe']['url']} for recipe in data['hits']]
    return render_template_string(HTML_TEMPLATE, recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
