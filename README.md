# 🥗 Nutrition Advisor — Microsoft Copilot Studio Skill

A production-ready **FastAPI** microservice that powers a **Microsoft Copilot Studio Skill** for nutrition guidance, calorie estimation, healthy food alternatives, and meal recommendations.

---

## 📁 Project Structure

```
nutrition-advisor/
├── app.py            # FastAPI application (all 4 endpoints + manifest route)
├── manifest.json     # Copilot Studio Skill manifest (Bot Framework v2.1 schema)
├── requirements.txt  # Python dependencies
├── render.yaml       # Render deployment configuration
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

### 1. `POST /meal-recommendation`
Returns a personalised meal suggestion based on diet type and goal.

**Request**
```json
{
  "dietType": "vegetarian",
  "goal": "weight loss"
}
```
**Response**
```json
{
  "mealSuggestion": "Paneer salad with cucumber and sprouts",
  "estimatedCalories": 350
}
```
Supported `dietType`: `vegetarian` · `vegan` · `non-vegetarian` · `keto`  
Supported `goal`: `weight loss` · `muscle gain` · `maintenance` · `diabetes control`

---

### 2. `POST /calorie-estimator`
Estimates calories for any described food item.

**Request**
```json
{ "foodItem": "2 rotis and dal" }
```
**Response**
```json
{ "estimatedCalories": 420 }
```

---

### 3. `POST /healthy-alternative`
Suggests a healthier substitute for a given food item.

**Request**
```json
{ "foodItem": "potato chips" }
```
**Response**
```json
{ "alternative": "roasted makhana (fox nuts) — crispy, light, and high in protein" }
```

---

### 4. `GET /nutrition-tip`
Returns a random evidence-based nutrition tip.

**Response**
```json
{
  "tip": "Drink a glass of water 20–30 minutes before meals to improve satiety and prevent overeating."
}
```

---

### Auto-generated OpenAPI docs

| URL | Purpose |
|-----|---------|
| `/docs` | Swagger UI |
| `/redoc` | ReDoc UI |
| `/openapi.json` | OpenAPI 3.0 schema |
| `/manifest.json` | Copilot Studio Skill manifest |

---

## 🚀 Local Development

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/nutrition-advisor.git
cd nutrition-advisor

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally
uvicorn app:app --reload

# API available at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

---

## 🐙 GitHub Deployment

```bash
# Initialise a new repo and push
git init
git add .
git commit -m "Initial commit: Nutrition Advisor Skill"
git branch -M main
git remote add origin https://github.com/<your-username>/nutrition-advisor.git
git push -u origin main
```

---

## ☁️ Render Deployment

1. Log in to [render.com](https://render.com) and click **New → Web Service**.
2. Connect your GitHub account and select the `nutrition-advisor` repository.
3. Render will auto-detect `render.yaml`. Confirm these settings:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Click **Create Web Service**. Render will assign a URL like:
   ```
   https://nutrition-advisor.onrender.com
   ```
5. Verify it is running:
   ```
   https://nutrition-advisor.onrender.com/docs
   https://nutrition-advisor.onrender.com/manifest.json
   ```

> ⚠️ **Free tier note:** Render free-tier services spin down after 15 minutes of inactivity. The first request after sleep may take ~30 seconds. Upgrade to a paid tier for always-on availability in production.

---

## 🔧 Exposing manifest.json

The manifest is served directly by the FastAPI app at the `/manifest.json` route — no static file hosting is needed. Once deployed on Render, it is accessible at:

```
https://nutrition-advisor.onrender.com/manifest.json
```

This is the URL you will paste into Copilot Studio when adding the skill.

---

## 🤖 Adding the Skill to Microsoft Copilot Studio

### Prerequisites
- A Microsoft 365 account with Copilot Studio access
- Your service deployed and accessible at the public URL

### Steps

1. Open [Copilot Studio](https://copilotstudio.microsoft.com) and open your agent (or create one).
2. In the left navigation, click **Settings → Skills**.
3. Click **Add a skill**.
4. Copy your **Agent ID** shown in the dialog (you may need it for the allow list on the skill side).
5. In the **Skill manifest URL** field, enter:
   ```
   https://nutrition-advisor.onrender.com/manifest.json
   ```
6. Click **Next** — Copilot Studio will fetch and validate the manifest.
7. Once validation passes, click **Add skill**.
8. The Nutrition Advisor skill actions will now appear in your agent's **Actions** list.

### Using the skill in topics

In any topic, add an **Action** node and select one of:
- `GetMealRecommendation` — pass `dietType` and `goal` variables
- `EstimateCalories` — pass `foodItem` variable
- `GetHealthyAlternative` — pass `foodItem` variable
- `GetNutritionTip` — no inputs required

---

## 🛠️ Configuration Notes

### Replacing placeholder values in `manifest.json`

After deployment, update `manifest.json` with your actual values:

| Field | Placeholder | Replace with |
|-------|-------------|--------------|
| `endpointUrl` | `https://nutrition-advisor.onrender.com/api/messages` | Your actual Bot Framework messaging endpoint |
| `msAppId` | `00000000-0000-0000-0000-000000000000` | Your Azure Bot App (client) ID |

> For pure REST/OpenAPI skills (no Bot Framework bot), Copilot Studio primarily uses the OpenAPI spec at `/openapi.json`. The manifest wraps it for discovery.

### Authentication

Currently set to **none** for testing. For production:
1. Register your app in **Azure Entra ID (App Registration)**.
2. Add the `msAppId` (Application client ID) to `manifest.json`.
3. Update `endpointUrl` to your secured Bot Framework endpoint.
4. In Copilot Studio Skills settings, provide the caller agent's app ID to the skill allow list.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.115.5 | Web framework |
| `uvicorn[standard]` | 0.32.1 | ASGI server |
| `pydantic` | 2.10.3 | Request / response validation |

---

## 📄 License

MIT — free to use, modify, and deploy.