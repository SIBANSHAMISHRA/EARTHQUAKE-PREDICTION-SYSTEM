import gradio as gr
import numpy as np
import joblib


clf, le = joblib.load('classifier.pkl')  # classifier 
reg = joblib.load('regressor.pkl')       # regressor

def predict(lat, lon, dep):
    try:
        features = np.array([[lat, lon, dep]])
        severity_idx = clf.predict(features)[0]
        severity_label = le.inverse_transform([severity_idx])[0]

        
        reverse_map = {
            'severe': 'mild',
            'moderate': 'moderate',
            'mild': 'severe'
        }
        severity = reverse_map.get(severity_label, severity_label)

        magnitude = reg.predict(features)[0]
        return f"Predicted Severity: {severity}", f"Predicted Magnitude: {magnitude:.2f}"
    except Exception as e:
        return f"Error: {str(e)}", ""


iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Latitude"),
        gr.Number(label="Longitude"),
        gr.Number(label="Depth")
    ],
    outputs=[
        gr.Textbox(label="Predicted Severity"),
        gr.Textbox(label="Predicted Magnitude")
    ],
    title="🌍 Earthquake Predictor (Live Data)",
    description="Predict earthquake severity & magnitude from real USGS data."
)


if __name__ == "__main__":
    iface.launch()
