# CPV Code Prediction API 🚀

## Overview
This project provides a **REST API** for predicting **CPV (Common Procurement Vocabulary) codes** based on procurement text descriptions. It utilizes **OpenAI's GPT-4o-mini** model to extract the first **5 digits** of the CPV code from given texts.

The API is built using **Flask**, containerized with **Docker**, and can be deployed easily with **Docker Compose**.

---

## Features ✅
- 📡 **REST API** for predicting CPV codes.
- 🧠 **Powered by OpenAI's GPT-4o-mini**.
- 📄 **Supports single and batch text inputs**.
- 🔄 **Retry mechanism** for handling rate limits.
- 📜 **Logging to both console and file**.
- 🐳 **Dockerized for easy deployment**.

---

## 📂 Project Structure
```
.
├── app
│   ├── main.py               # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── logs                   # Directory for log files
│   ├── Dockerfile             # Docker setup
│   ├── config.py              # Configuration settings (optional)
│   ├── __init__.py            # Package initialization (if needed)
│   └── tests                  # Unit tests (if needed)
│
├── docker-compose.yml          # Docker Compose configuration
├── README.md                   # Project documentation
└── .gitignore                  # Ignore unnecessary files
```

---

## 🛠 Installation & Setup

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/cpv-prediction-api.git
cd cpv-prediction-api
```

### 2️⃣ **Set Up Virtual Environment (Optional)**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```sh
pip install -r app/requirements.txt
```

### 4️⃣ **Run the API Locally**
```sh
python app/main.py
```
- The API will be available at `http://localhost:5000`

---

## 🐳 Run with Docker
### **1️⃣ Build the Docker Image**
```sh
docker build -t cpv-api .
```
### **2️⃣ Run the API in a Container**
```sh
docker run -p 5000:5000 cpv-api
```

### **3️⃣ Run with Docker Compose**
```sh
docker-compose up --build
```

---

## 🔥 API Usage
### **Request Format**
The API expects a **POST request** with a JSON payload containing:
- `api_key`: Your OpenAI API key.
- `texts`: A **list** of text descriptions (or a single string) to predict CPV codes.

### **Example Request (cURL)**
```sh
curl -X POST "http://localhost:5000/predict" -H "Content-Type: application/json" -d '{
  "api_key": "sk-YOUR-OPENAI-KEY",
  "texts": ["Servicios de mantenimiento de parques", "Reparación de carreteras"]
}'
```

### **Example Response**
```json
[
  {
    "text": "Servicios de mantenimiento de parques",
    "cpv_code": "77311"
  },
  {
    "text": "Reparación de carreteras",
    "cpv_code": "45233"
  }
]
```

---

## 📜 Logging
- All logs are stored in the **`app/logs`** directory.
- You can check logs in real-time while running the API.

```sh
tail -f app/logs/cpv_api.log
```

---

## 🧪 Testing the API
To verify the API is working correctly, you can:
1. **Use Postman**:  
   - Set the **method** to `POST`.  
   - Enter `http://localhost:5000/predict` as the **URL**.  
   - Add a **JSON body**:
     ```json
     {
       "api_key": "sk-YOUR-OPENAI-KEY",
       "texts": ["Servicios de mantenimiento de parques", "Reparación de carreteras"]
     }
     ```
   - Click **Send** and check the response.

2. **Use cURL** (from the terminal):
   ```sh
   curl -X POST "http://localhost:5000/predict" -H "Content-Type: application/json" -d '{
     "api_key": "sk-YOUR-OPENAI-KEY",
     "texts": ["Servicios de mantenimiento de parques", "Reparación de carreteras"]
   }'
   ```

---

## 🔄 Stopping & Removing Containers
If you need to stop the running Docker containers:
```sh
docker-compose down
```
To remove all Docker containers and images related to this project:
```sh
docker system prune -a
```
