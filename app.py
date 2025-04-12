from flask import Flask, request, jsonify
from transformers import pipeline

# Inisialisasi Flask dan GPT-2
app = Flask(__name__)
generator = pipeline('text-generation', model='gpt2')

# Tempat penyimpanan data suhu terakhir
latest_data = {
    "temperature": None,
    "description": "No data yet"
}

# Route untuk menerima data suhu dari ESP32
@app.route('/temperature', methods=['POST'])
def receive_temperature():
    try:
        data = request.get_json()
        temp = data.get('temperature')

        if temp is None:
            return jsonify({"error": "Temperature not provided"}), 400

        # Buat prompt dan generate deskripsi AI
        prompt = f"Today's temperature is {temp} degrees Celsius. Briefly describe how the weather feels at {temp} degrees in one or two short sentences."
        result = generator(prompt, max_length=50, num_return_sequences=1)
        description = result[0]['generated_text']

        # Simpan data terakhir
        latest_data["temperature"] = temp
        latest_data["description"] = description

        return jsonify({
            "message": "Data received successfully",
            "temperature": temp,
            "description": description
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route untuk mengakses data suhu terakhir
@app.route('/latest', methods=['GET'])
def get_latest():
    if latest_data["temperature"] is None:
        return jsonify({"error": "No data available yet"}), 204  # No content
    return jsonify(latest_data)

# Jalankan server Flask
if __name__ == '__main__':
    # 0.0.0.0 agar bisa diakses dari jaringan lokal (ESP32 & Streamlit)
    app.run(host='0.0.0.0', port=5000)
