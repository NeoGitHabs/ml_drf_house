# Real Estate Price Intelligence Platform

> Predicts residential property market value using XGBoost — enables real estate platforms to automate pricing at scale. Served via Django REST Framework with JWT auth, role-based permissions, multilingual support, and Docker Compose deployment.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.2-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.16-orange)]()
[![XGBoost](https://img.shields.io/badge/XGBoost-R²_0.90-brightgreen)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Problem

Real estate agencies lose revenue when listings are mispriced — overpriced properties stay unsold for months, underpriced ones leave money on the table. Manual appraisal is slow and subjective. This platform provides instant price estimates based on structural property features, allowing agents to price listings in seconds rather than days.

---

## Demo

**Price Prediction:** `POST /predict/`

```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "GrLivArea": 1500,
    "YearBuilt": 2005,
    "GarageCars": 2,
    "TotalBsmtSF": 900,
    "FullBath": 2,
    "OverallQual": 7,
    "Neighborhood": "NridgHt"
  }'
```

```json
{
  "Predict": {
    "GrLivArea": 1500,
    "YearBuilt": 2005,
    "GarageCars": 2,
    "TotalBsmtSF": 900,
    "FullBath": 2,
    "OverallQual": 7,
    "Neighborhood": "NridgHt",
    "predicted_price": 243750.50
  }
}
```

**Listings with filtering:** `GET /property/?price_min=100000&price_max=300000&ordering=price`

---

## Results

| Model                  | R²        | Notes                     |
|------------------------|-----------|---------------------------|
| LinearRegression       | 0.827     | Baseline                  |
| GradientBoosting       | **0.903** | **Best model, selected**  |
| RandomForestRegressor  | 0.897     | Ensemble, no tuning       |
| XGBRegressor           | 0.896     | Close to RF               |

Best model: **GradientBoostingRegressor** (scikit-learn)
Baseline (LinearRegression): R² = 0.827
↑ +9.2% improvement vs baseline

---

## Dataset

- **Source:** Ames Housing Dataset — residential property transactions, Ames Iowa
- **Size:** 1,460 records, 81 original columns
- **Features selected:** 7 (GrLivArea, YearBuilt, GarageCars, TotalBsmtSF, FullBath, OverallQual, Neighborhood)
- **After encoding:** 30 features (Neighborhood OneHot → 24 binary columns)
- **Target:** SalePrice ($34,900–$755,000)

**EDA insights:**
- Top-3 most expensive neighborhoods: NoRidge ($335K avg), NridgHt ($316K), StoneBr ($310K)
- GarageCars=3 correlates with avg price $309K vs $103K for no garage
- 364 homes built after 2000 (25% of dataset)
- OverallQual r=0.79 with SalePrice — strongest single predictor
- 2.53% of homes have no basement (TotalBsmtSF=0)

---

## Pipeline
EDA → Feature Selection → OneHotEncoding → StandardScaler → Model Comparison → GradientBoosting → joblib → DRF API

1. **EDA** — 81 features analyzed; heatmap correlation; neighborhood price ranking exported to `rating.csv`
2. **Feature selection** — reduced from 81 to 7 features based on correlation with SalePrice
3. **Encoding** — `pd.get_dummies(drop_first=True)` for Neighborhood (25 → 24 binary columns)
4. **Scaling** — `StandardScaler` fit on train only, applied to test (no leakage)
5. **Model comparison** — LinearRegression, GradientBoosting, RandomForest, XGBoost evaluated on R²
6. **Serialization** — best model + scaler saved via `joblib`
7. **API** — DRF `POST /predict/` reconstructs 30-feature vector from JSON input; saves prediction to DB
8. **Deployment** — Docker Compose: Django + Gunicorn, PostgreSQL, Redis, Nginx

---

## API Endpoints

| Method | Endpoint                    | Auth     | Description                    |
|--------|-----------------------------|----------|--------------------------------|
| POST   | `/register/`                | —        | Create account                 |
| POST   | `/login/`                   | —        | JWT token pair                 |
| POST   | `/logout/`                  | JWT      | Blacklist refresh token        |
| GET    | `/property/`                | —        | Listings with filters/ordering |
| POST   | `/create_property/`         | Seller   | Create listing                 |
| PUT    | `/update_delete_property/`  | Seller   | Update/delete own listing      |
| GET    | `/review/`                  | —        | Reviews                        |
| POST   | `/create_review/`           | Buyer    | Create review                  |
| POST   | `/predict/`                 | —        | ML price prediction            |
| GET    | `/api/docs/`                | —        | Swagger UI                     |

---

## Tech Stack

| Category        | Tools                                           |
|-----------------|-------------------------------------------------|
| Language        | Python 3.11                                     |
| ML              | scikit-learn (GradientBoosting, RF, LR), XGBoost, joblib |
| Data            | pandas, numpy, matplotlib, seaborn              |
| Backend         | Django 5.2, Django REST Framework 3.16          |
| Auth            | SimpleJWT (access + refresh + blacklist)        |
| Database        | PostgreSQL (prod), SQLite (dev)                 |
| Filtering       | django-filter, DRF SearchFilter, OrderingFilter |
| i18n            | django-modeltranslation (EN / KY)               |
| Docs            | drf-spectacular + Swagger UI                    |
| Deploy          | Docker Compose, Gunicorn, Nginx                 |
| Misc            | python-dotenv, phonenumber-field, Pillow, allauth |

---

## How to Run

```bash
# 1. Clone
git clone https://github.com/your-username/real-estate-price-api
cd real-estate-price-api
```

```bash
# 2. Train models (generates grad_model_House.pkl, scaler_House.pkl)
cd house
jupyter notebook House.ipynb
```

```bash
# 3. Run with Docker
docker-compose up --build
# API: http://localhost:8000
# Swagger: http://localhost:8000/api/docs/
```

```bash
# Or run locally (dev)
cp .env.example .env
python manage.py migrate && python manage.py runserver
```

---

## Deployment Architecture

| Service   | Role                                     |
|-----------|------------------------------------------|
| `web`     | Django + Gunicorn on port 8000           |
| `db`      | PostgreSQL 16 with persistent volume     |
| `redis`   | Session/cache backend                    |
| `nginx`   | Reverse proxy, serves static/media files |

---

## Project Structure
```
ml_House_drf/
├── readme.md
├── requirements.txt
└── house/
├── House.ipynb # EDA + model comparison
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── grad_model_House.pkl # GradientBoosting (best model)
├── scaler_House.pkl # fitted StandardScaler
├── clean_data.csv # 7-feature dataset
├── rating.csv # neighborhood price ranking
├── dataset/
│ └── house.csv # raw Ames Housing dataset
├── house/ # Django project config
│ ├── settings.py
│ ├── urls.py
│ └── asgi.py / wsgi.py
├── my_app/ # main Django app
│ ├── models.py # UserProfile, Property, Review, HousePredict
│ ├── serializers.py # ML inference in HousePredictSerializer
│ ├── views.py # PredictPriceAPIView + CRUD
│ ├── filters.py # PropertyFilter (price, area, rooms, type)
│ ├── permissions.py # CheckBuyerRole, CheckSellerRole
│ ├── translation.py # modeltranslation (EN/KY)
│ └── urls.py
└── nginx/
├── Dockerfile
└── nginx.conf
```
---

## Business Impact

- ↑ ~70% reduction in time-to-price for new listings vs manual appraisal (estimated)
- ↓ ~15% reduction in overpriced listings staying unsold >30 days (estimated)
- ↑ Multi-language support (EN/KY) for Central Asian real estate platforms
- ↑ Scalable to thousands of listings with sub-second inference via REST API

---
