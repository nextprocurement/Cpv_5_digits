import logging
import json
import os
import time
from flask import Flask, request, jsonify
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai.chat_models import ChatOpenAI

# -----------------------------
# ✅ Logging Configuration
# -----------------------------

# Create a "logs" directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Log file path
log_filename = os.path.join(log_dir, "cpv_api.log")

# Configure logging to both the console and a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Save logs to a file
        logging.StreamHandler()  # Display logs in the terminal
    ]
)

# -----------------------------
# ✅ Initialize Flask Application
# -----------------------------
app = Flask(__name__)

# -----------------------------
# ✅ Configuration for API Rate Limit Handling
# -----------------------------
retry_wait_time = 30  # Wait time before retrying in case of rate limit (seconds)
max_retries = 3  # Maximum number of retries before failing

# -----------------------------
# ✅ Function to Predict CPV Code
# -----------------------------

def get_cpv_code(objective_text, api_key):
    """
    Queries the OpenAI model to predict the CPV code from a given text.
    
    - objective_text: The input text to predict the CPV code.
    - api_key: The API key to authenticate the OpenAI request.

    Returns:
    - A 5-digit CPV code if the prediction is successful.
    - None if the model fails or the prediction is invalid.
    """

    # Set the OpenAI API key for the session
    os.environ["OPENAI_API_KEY"] = api_key

    # Initialize the OpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")

    attempt = 0  # Attempt counter

    while attempt < max_retries:
        try:
            # Create the prompt for the model
            prompt_template = ChatPromptTemplate.from_messages(
                [
                    SystemMessagePromptTemplate.from_template("Eres un experto en codificación CPV. Debes proporcionar únicamente códigos CPV válidos de 5 dígitos."),
                    HumanMessagePromptTemplate.from_template(
                        "Dado el siguiente texto: '{objective_text}', proporciona solo los primeros 5 dígitos del código CPV. "
                        "Debe ser un número de exactamente 5 dígitos. Solo números, sin texto adicional ni espacios.\n\n"
                        "Ejemplo:\n"
                        "Texto: 'Servicios de mantenimiento de parques.'\n"
                        "Respuesta: 77311"
                    )
                ]
            )

            # Format the message
            prompt = prompt_template.format_messages(objective_text=objective_text)

            # Call the OpenAI model
            response = model(prompt)

            # Extract the generated text response
            cpv_code = response.content.strip()

            # Keep only numeric characters
            cpv_code_filtered = ''.join(filter(str.isdigit, cpv_code))

            # Adjust the length of the CPV code
            if len(cpv_code_filtered) > 5:
                cpv_code_filtered = cpv_code_filtered[:5]
            elif len(cpv_code_filtered) == 4:
                cpv_code_filtered += '0'

            # Validate that the final CPV code is exactly 5 digits
            return cpv_code_filtered if len(cpv_code_filtered) == 5 else None

        except Exception as e:
            logging.error(f"Error processing text '{objective_text}': {e}")

            # Handle OpenAI rate limit errors
            if "rate_limit_exceeded" in str(e):
                attempt += 1
                logging.warning(f"Rate limit reached. Retrying in {retry_wait_time} seconds... (Attempt {attempt}/{max_retries})")
                time.sleep(retry_wait_time)
            else:
                return None  # If an error other than rate limit occurs, return None immediately

    logging.error(f"Max retries reached for text: {objective_text}")
    return None  # If max retries are reached, return None

# -----------------------------
# ✅ API Endpoint for CPV Prediction
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():
    """
    API endpoint to predict CPV codes.

    - Expects a JSON payload with:
        - "api_key": The OpenAI API key.
        - "texts": A list of texts to process.

    - Returns a JSON response with the CPV codes.
    """

    # Parse request JSON data
    data = request.get_json()

    # Validate required parameters
    if not data or "api_key" not in data or "texts" not in data:
        return jsonify({"error": "Missing required fields: 'api_key' and 'texts'"}), 400

    api_key = data["api_key"]
    texts = data["texts"]

    # Convert to list if only a single text is provided
    if not isinstance(texts, list):
        texts = [texts]

    results = []
    for text in texts:
        cpv_code = get_cpv_code(text, api_key)
        results.append({"text": text, "cpv_code": cpv_code})

    return jsonify(results)

# -----------------------------
# ✅ Run Flask Application
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
