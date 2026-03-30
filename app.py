import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model_nb.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]

    prediction = model.predict(final_features)
    proba = model.predict_proba(final_features)

    output = round(prediction[0], 2)

    return jsonify(prediction_text=format(output), proba=format(proba))

@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    #prediction = model.predict_proba([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)

@app.route('/api/', methods=['POST'])
def makecalc():
    j_data = request.get_json()
    #prediction = np.array2string(model.predict(j_data))
    prediction = np.array2string(model.predict_proba(j_data))
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)
