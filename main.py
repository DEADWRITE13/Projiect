import json
from flask import Flask, render_template, request, jsonify, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from model import SkateboardModel
from decimal import Decimal  # Import Decimal

app = Flask(__name__)
app.debug = True

# Конфигурация БД
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1234"  # Замените на правильный пароль
}

# Папка для изображений
app.config['UPLOAD_FOLDER'] = 'static/images/scatesRecomendation'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def main():
    return render_template("main.html")

@app.route('/results')
def show_results():
    try:
        with open('static/recommendations.json', 'r') as f:
            data = json.load(f)
            params = data['parameters']
            recommendations = data['recommendations']
        return render_template('otvet.html', params=params, recommendations=recommendations)
    except Exception as e:
        app.logger.error(f"Error loading recommendations: {e}")
        return "Error loading recommendations", 500

# Custom JSON encoder to handle Decimal objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Or str(obj) if you prefer
        return super().default(obj)

app.json_encoder = CustomJSONEncoder  # Set the custom encoder

@app.route('/api/recommend', methods=['POST'])
def recommend_skateboards():
    try:
        data = request.get_json()

        # Валидация данных
        weight = int(data.get('weight'))
        budget = float(data.get('budget'))
        purposes = data.get('purposes')

        print("Weight from form:", weight)
        print("Budget from form:", budget)
        print("Purposes from form:", purposes)

        if not purposes:
            return jsonify({'success': False, 'error': 'Выберите цель использования'}), 400

        # Берем первое значение из списка (если multiple=False в форме)
        purpose_id = str(purposes[0] if isinstance(purposes, list) else purposes)
        print("Purpose ID from form:", purpose_id)

        # Получаем рекомендации из БД
        recommendations = []
        with SkateboardModel(DB_CONFIG) as model:
            skateboards = model.get_filtered_skateboards(
                weight=weight,
                budget=budget,
                purpose_id=purpose_id
            )

            for skate in skateboards:
                #image_name = f"{secure_filename(skate['name'].lower().replace(' ', '_'))}.jpg"
                #image_path = url_for('static', filename=os.path.join('images', 'scatesRecomendation', image_name))

                #if not os.path.exists(os.path.join(app.static_folder,image_path[len(url_for('static', filename='')):])):  # remove static
                #    image_path = url_for('static', filename=os.path.join('images', 'scatesRecomendation', 'default.jpg'))
                #image_path = url_for('static', filename=skate['urlimage'])  # Используем путь из базы данных
                image_path = skate['urlimage'] # Используем путь из базы данных

                recommendations.append({
                    'name': skate['name'],
                    'price': float(skate['cost']),  # Convert Decimal to float
                    'weight': skate['ves'],
                    'link': skate['url'],
                    'image': image_path
                })

        # Сохраняем параметры и рекомендации в файл
        user_params = {
            'weight': weight,
            'purpose': purpose_id,
            'budget': budget
        }

        recommendation_data = {
            'parameters': user_params,
            'recommendations': recommendations,
            'generated_at': datetime.now().isoformat()
        }

        with open('static/recommendations.json', 'w') as f:
            json.dump(recommendation_data, f, indent=4, ensure_ascii=False, cls=CustomJSONEncoder)  # Using CustomJSONEncoder

        return jsonify({
            'success': True,
            'params': user_params,
            'recommendations': recommendations
        })

    except Exception as e:
        app.logger.error(f"Error in recommend_skateboards: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)