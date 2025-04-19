from flask import Flask, request, jsonify
import pandas as pd
import statsmodels.api as sm


app = Flask(__name__)

# training data
data = {
    'Y': [137, 118, 124, 124, 120, 129, 122, 142, 128, 114, 132, 130, 130, 112, 132, 117, 134, 132, 121, 128],
    'W': [0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    'X': [19.8, 23.4, 27.7, 24.6, 21.5, 25.1, 22.4, 29.3, 20.8, 20.2, 27.3, 24.5, 22.9, 18.4, 24.2, 21, 25.9, 23.2, 21.6, 22.8]
}

df = pd.DataFrame(data)
# Prepare the independent and dependent variables
X = sm.add_constant(df[['W', 'X']])  # Add constant for intercept
Y = df['Y']

# Fit the OLS model
model = sm.OLS(Y, X).fit()
print(model.summary())

@app.route("/predict")
def predict():
    w = int(request.args.get("w", 0))
    x = float(request.args.get("x", 0))
    input_combined = pd.DataFrame({'const': 1, 'W': [w], 'X': [x]})

    y_pred = model.predict(input_combined)[0]
  
    # Log prediction
    with open("output.txt", "w") as f:
      f.write(f"Input w:{w} x: {x}\nPrediction: {y_pred}\n")
    return jsonify({"w": w, "x": x, "prediction": y_pred}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
