"""
Nutrition Advisor Skill — FastAPI backend
Copilot Studio Skill Manifest URL: https://nutrition-advisor.onrender.com/manifest.json
"""

import json
import random
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ── App Setup ──────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Nutrition Advisor Skill",
    version="1.0.0",
    description="Provides nutrition guidance, calorie estimation, healthy food alternatives, and meal recommendations.",
    contact={
        "name": "Nutrition Advisor",
        "url": "https://nutrition-advisor.onrender.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response Models ──────────────────────────────────────────────────

class MealRecommendationRequest(BaseModel):
    dietType: str
    goal: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"dietType": "vegetarian", "goal": "weight loss"}
            ]
        }
    }

class MealRecommendationResponse(BaseModel):
    mealSuggestion: str
    estimatedCalories: int


class CalorieEstimatorRequest(BaseModel):
    foodItem: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"foodItem": "2 rotis and dal"}
            ]
        }
    }

class CalorieEstimatorResponse(BaseModel):
    estimatedCalories: int


class HealthyAlternativeRequest(BaseModel):
    foodItem: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"foodItem": "potato chips"}
            ]
        }
    }

class HealthyAlternativeResponse(BaseModel):
    alternative: str


class NutritionTipResponse(BaseModel):
    tip: str


# ── Data ───────────────────────────────────────────────────────────────────────

MEAL_DB: dict[str, dict[str, dict]] = {
    "vegetarian": {
        "weight loss":       {"mealSuggestion": "Paneer salad with cucumber and sprouts",          "estimatedCalories": 350},
        "muscle gain":       {"mealSuggestion": "Paneer bhurji with whole wheat toast and milk",   "estimatedCalories": 520},
        "maintenance":       {"mealSuggestion": "Dal tadka with brown rice and salad",              "estimatedCalories": 460},
        "diabetes control":  {"mealSuggestion": "Moong dal chilla with mint chutney",              "estimatedCalories": 280},
        "default":           {"mealSuggestion": "Mixed vegetable khichdi with low-fat curd",        "estimatedCalories": 390},
    },
    "vegan": {
        "weight loss":       {"mealSuggestion": "Quinoa bowl with roasted vegetables and tahini",  "estimatedCalories": 340},
        "muscle gain":       {"mealSuggestion": "Chickpea curry with brown rice and almonds",      "estimatedCalories": 580},
        "maintenance":       {"mealSuggestion": "Tofu stir fry with millets and steamed broccoli", "estimatedCalories": 450},
        "default":           {"mealSuggestion": "Lentil soup with whole grain bread",              "estimatedCalories": 380},
    },
    "non-vegetarian": {
        "weight loss":       {"mealSuggestion": "Grilled chicken breast with steamed vegetables",  "estimatedCalories": 370},
        "muscle gain":       {"mealSuggestion": "Egg white omelette with chicken and whole toast", "estimatedCalories": 560},
        "maintenance":       {"mealSuggestion": "Fish curry with brown rice and salad",            "estimatedCalories": 480},
        "default":           {"mealSuggestion": "Boiled eggs with dal and chapati",               "estimatedCalories": 430},
    },
    "keto": {
        "weight loss":       {"mealSuggestion": "Avocado and paneer bowl with olive oil dressing", "estimatedCalories": 420},
        "muscle gain":       {"mealSuggestion": "Egg and cheese omelette with bulletproof coffee", "estimatedCalories": 600},
        "default":           {"mealSuggestion": "Cauliflower rice with grilled paneer",           "estimatedCalories": 390},
    },
}

CALORIE_DB: dict[str, int] = {
    "2 rotis and dal":            420,
    "roti":                       120,
    "rice":                       200,
    "biryani":                    550,
    "samosa":                     260,
    "idli":                       70,
    "dosa":                       170,
    "poha":                       250,
    "upma":                       220,
    "paratha":                    280,
    "chole bhature":              620,
    "rajma chawal":               480,
    "dal makhani":                360,
    "palak paneer":               320,
    "chicken biryani":            600,
    "egg bhurji":                 220,
    "banana":                     90,
    "apple":                      80,
    "mango":                      100,
    "chai":                       80,
    "lassi":                      180,
    "buttermilk":                 70,
    "potato chips":               520,
    "burger":                     490,
    "pizza slice":                285,
    "chocolate":                  550,
}

ALTERNATIVE_DB: dict[str, str] = {
    "potato chips":    "roasted makhana (fox nuts) — crispy, light, and high in protein",
    "burger":          "multigrain veggie wrap with hummus and greens",
    "pizza":           "whole wheat pita with homemade tomato sauce and paneer",
    "chocolate":       "a square of 85%+ dark chocolate or a date-nut energy ball",
    "samosa":          "baked mini rajma or paneer stuffed pockets",
    "white rice":      "brown rice or millet (bajra / jowar) for more fibre",
    "white bread":     "whole grain or multigrain bread with seeds",
    "fried poori":     "baked whole wheat poori or steamed appam",
    "ice cream":       "frozen banana nice-cream or low-fat yogurt with fruit",
    "cold drink":      "nimbu pani (lemonade) with sabja seeds or plain coconut water",
    "maggi noodles":   "oat noodles or vegetable poha with the same seasonings",
    "biscuits":        "roasted chana, murmura, or a small handful of mixed nuts",
    "deep fried snacks": "air-fried or baked snacks with the same spice profile",
    "mayonnaise":      "hung curd dip or avocado spread",
    "full cream milk": "low-fat milk or unsweetened almond / oat milk",
}

NUTRITION_TIPS: list[str] = [
    "Drink a glass of water 20–30 minutes before meals to improve satiety and prevent overeating.",
    "Fill half your plate with vegetables, a quarter with whole grains, and a quarter with lean protein.",
    "Eating slowly and chewing well helps digestion and signals fullness to your brain.",
    "Swap refined grains (maida) for whole grains (atta, millets) to increase fibre intake.",
    "Include a source of protein — dal, paneer, eggs, or legumes — in every main meal.",
    "Limit sugary beverages; even fruit juice spikes blood sugar. Prefer whole fruit instead.",
    "A handful of mixed nuts makes a satisfying snack that keeps energy stable between meals.",
    "Eating at consistent times each day supports your metabolism and reduces late-night cravings.",
    "Dark leafy greens like spinach and methi are rich in iron and folate — eat them daily.",
    "Turmeric (haldi) has anti-inflammatory properties; add a pinch to warm milk or dal.",
    "Sprouts are a low-calorie, high-protein breakfast option — try moong, chana, or masoor.",
    "Avoid eating while watching screens; distracted eating typically leads to 25% more calorie intake.",
]


def _lookup_meal(diet_type: str, goal: str) -> dict:
    """Return best-match meal from MEAL_DB with fuzzy fallback."""
    diet_key = diet_type.lower().strip()
    goal_key = goal.lower().strip()
    diet_map = MEAL_DB.get(diet_key, MEAL_DB.get("vegetarian", {}))
    return diet_map.get(goal_key, diet_map.get("default", {
        "mealSuggestion": "Seasonal vegetable bowl with dal and brown rice",
        "estimatedCalories": 400,
    }))


def _estimate_calories(food_item: str) -> int:
    """Return calorie estimate; fuzzy match on key substrings."""
    key = food_item.lower().strip()
    if key in CALORIE_DB:
        return CALORIE_DB[key]
    for db_key, cal in CALORIE_DB.items():
        if db_key in key or key in db_key:
            return cal
    # Generic fallback: ~150 cal per described item
    word_count = len(key.split())
    return max(150, min(800, word_count * 120 + random.randint(-30, 30)))


def _find_alternative(food_item: str) -> str:
    """Return healthy alternative; fuzzy match on key substrings."""
    key = food_item.lower().strip()
    if key in ALTERNATIVE_DB:
        return ALTERNATIVE_DB[key]
    for db_key, alt in ALTERNATIVE_DB.items():
        if db_key in key or key in db_key:
            return alt
    return f"a baked or steamed version of {food_item} with less oil and no added salt"


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"], summary="Health check")
async def root():
    return {"status": "ok", "service": "Nutrition Advisor Skill"}


@app.post(
    "/meal-recommendation",
    response_model=MealRecommendationResponse,
    tags=["Nutrition"],
    summary="Get a personalised meal recommendation",
    operation_id="getMealRecommendation",
)
async def meal_recommendation(req: MealRecommendationRequest):
    """
    Returns a meal suggestion and estimated calories based on diet type and health goal.

    Supported **dietType** values: `vegetarian`, `vegan`, `non-vegetarian`, `keto`

    Supported **goal** values: `weight loss`, `muscle gain`, `maintenance`, `diabetes control`
    """
    result = _lookup_meal(req.dietType, req.goal)
    return MealRecommendationResponse(**result)


@app.post(
    "/calorie-estimator",
    response_model=CalorieEstimatorResponse,
    tags=["Nutrition"],
    summary="Estimate calories for a food item",
    operation_id="estimateCalories",
)
async def calorie_estimator(req: CalorieEstimatorRequest):
    """
    Returns an estimated calorie count for the described food item or meal.

    Example inputs: `"2 rotis and dal"`, `"chicken biryani"`, `"banana"`, `"samosa"`
    """
    calories = _estimate_calories(req.foodItem)
    return CalorieEstimatorResponse(estimatedCalories=calories)


@app.post(
    "/healthy-alternative",
    response_model=HealthyAlternativeResponse,
    tags=["Nutrition"],
    summary="Suggest a healthy alternative to a food item",
    operation_id="getHealthyAlternative",
)
async def healthy_alternative(req: HealthyAlternativeRequest):
    """
    Returns a healthier substitute for the provided food item.

    Example inputs: `"potato chips"`, `"burger"`, `"white rice"`, `"cold drink"`
    """
    alt = _find_alternative(req.foodItem)
    return HealthyAlternativeResponse(alternative=alt)


@app.get(
    "/nutrition-tip",
    response_model=NutritionTipResponse,
    tags=["Nutrition"],
    summary="Get a random daily nutrition tip",
    operation_id="getNutritionTip",
)
async def nutrition_tip():
    """Returns a random evidence-based nutrition tip."""
    return NutritionTipResponse(tip=random.choice(NUTRITION_TIPS))


# ── Manifest endpoint ──────────────────────────────────────────────────────────

@app.get(
    "/manifest.json",
    tags=["Skill"],
    summary="Copilot Studio skill manifest",
    include_in_schema=False,
)
async def get_manifest():
    """Serves the Bot Framework v2.1 skill manifest for Copilot Studio."""
    manifest_path = Path(__file__).parent / "manifest.json"
    data = json.loads(manifest_path.read_text())
    return JSONResponse(content=data)