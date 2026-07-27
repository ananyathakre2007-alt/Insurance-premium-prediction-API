# 🏥 Insurance Premium Prediction API

A Machine Learning REST API built with **FastAPI** to predict an insurance premium category based on user information.

## 🚀 Features

- FastAPI backend
- Pydantic input validation
- Automatic feature engineering (BMI, Age Group, Lifestyle Risk, City Tier)
- Scikit-learn model integration
- Interactive API documentation with Swagger

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- Scikit-learn
- Pandas
- NumPy
- Uvicorn

## 📦 Installation

```bash
git clone <repository-url>
cd insurance-premium-prediction-api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## ▶️ Run the API

```bash
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

## 📌 API Endpoint

**POST** `/predict`

Returns the predicted insurance premium category based on the provided user details.

## 📄 License

This project is for learning and educational purposes.
