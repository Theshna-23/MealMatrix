"""
utils.py - Core Engine for Meal Matrix
Includes:
- Dynamic recipe generator & translation
- Smart Recipe Scaler & Cost Estimator
- Intelligent Culinary Substitute Engine
- Nutrition & Diabetic / Low-GI Health Indexer
- 1-Click WhatsApp Grocery List Generator
- Pantry matching algorithm
"""

import re
import urllib.parse
from typing import List, Dict, Any, Tuple
from deep_translator import GoogleTranslator
from recipes import BUILTIN_RECIPES

# Translator instance
translator = GoogleTranslator(source='en', target='ta')

# -----------------------------------------------------------------------------
# 1. CULINARY SUBSTITUTE DATABASE
# -----------------------------------------------------------------------------
SUBSTITUTES_DB = {
    "tamarind": {
        "alternatives": [
            "1.5 tbsp Fresh Lemon Juice (add at the very end off heat)",
            "1 Chopped Raw Green Mango (simmer along with dal)",
            "1 tsp Amchur / Dry Mango Powder"
        ],
        "taste_profile": "Sour / Tangy"
    },
    "ghee": {
        "alternatives": [
            "Cold-pressed Coconut Oil or Sesame Oil (1:1 ratio)",
            "Unsalted Butter (equal measure)",
            "Neutral Vegetable Oil + pinch of cumin"
        ],
        "taste_profile": "Rich / Nutty"
    },
    "paneer": {
        "alternatives": [
            "Firm Tofu (high protein, lower fat, vegan)",
            "Boiled Chickpeas or Button Mushrooms",
            "Pan-fried Potato Cubes (Aloo)"
        ],
        "taste_profile": "Mild Dairy Protein"
    },
    "curd": {
        "alternatives": [
            "Plain Unsweetened Yogurt or Greek Yogurt diluted with water",
            "Buttermilk (reduce other added liquids by 50ml)",
            "Cashew Cream + 1 tsp lemon juice (vegan option)"
        ],
        "taste_profile": "Creamy / Acidic"
    },
    "tomato": {
        "alternatives": [
            "1 tbsp Tomato Paste + 3 tbsp warm water",
            "1 tbsp Tamarind Extract + pinch of jaggery",
            "Pureed Red Bell Pepper + 1/2 tsp vinegar"
        ],
        "taste_profile": "Umami / Acidic"
    },
    "ginger garlic paste": {
        "alternatives": [
            "1.5 tsp grated fresh ginger + 1 tsp minced fresh garlic",
            "1/2 tsp dry ginger powder + 1/2 tsp garlic powder",
            "Crushed shallots and ginger (if garlic-free)"
        ],
        "taste_profile": "Aromatic Pungency"
    },
    "cream": {
        "alternatives": [
            "Soaked Cashew Paste (15 cashews blended with 30ml warm water)",
            "Full-fat Coconut Milk (especially in South Indian curries)",
            "Equal parts milk and whisked butter"
        ],
        "taste_profile": "Richness & Thickness"
    },
    "asafoetida": {
        "alternatives": [
            "Pinch of garlic powder + onion powder",
            "Finely minced leeks or shallots",
            "Skip safely if gluten-sensitive"
        ],
        "taste_profile": "Savory / Allium Aroma"
    }
}


def find_ingredient_substitute(ingredient_name: str) -> Dict[str, Any]:
    """Finds culinary substitutes for a given ingredient."""
    clean_name = ingredient_name.lower()
    for key, data in SUBSTITUTES_DB.items():
        if key in clean_name:
            return data
    return {
        "alternatives": [
            "Can be omitted without altering the core structure",
            "Substitute with a pinch of generic garam masala or lemon juice for balance"
        ],
        "taste_profile": "Standard Seasoning"
    }


# -----------------------------------------------------------------------------
# 2. RECIPE SCALER & COST ESTIMATOR
# -----------------------------------------------------------------------------
# Average benchmark prices in INR (₹) per 100g or 100ml in Indian markets
ESTIMATED_PRICE_PER_100G = {
    "dal": 16.0,
    "rice": 7.0,
    "ghee": 70.0,
    "oil": 18.0,
    "paneer": 45.0,
    "vegetable": 6.0,
    "tomato": 4.0,
    "onion": 5.0,
    "garlic": 25.0,
    "cashew": 110.0,
    "spice": 20.0,
    "chicken": 26.0,
    "default": 10.0
}


def scale_quantity_string(qty_str: str, multiplier: float) -> str:
    """Scales numbers found in quantity strings proportionally."""
    def replacer(match):
        val = float(match.group())
        scaled = round(val * multiplier, 1)
        return f"{scaled:g}"
    return re.sub(r"\d+(\.\d+)?", replacer, qty_str)


def calculate_cost_and_scaled_ingredients(ingredients: List[Dict[str, str]], base_servings: int, target_servings: int) -> Tuple[List[Dict[str, str]], float]:
    """Scales all ingredients and estimates the total grocery cost in INR."""
    multiplier = target_servings / base_servings
    scaled_list = []
    total_cost_inr = 0.0

    for ing in ingredients:
        original_qty = ing["quantity"]
        scaled_qty = scale_quantity_string(original_qty, multiplier)

        # Estimate grams from quantity string for costing
        numbers = re.findall(r"\d+(?:\.\d+)?", original_qty)
        qty_num = float(numbers[0]) if numbers else 10.0
        scaled_weight = qty_num * multiplier

        # Detect category price
        name_lower = ing["name_en"].lower()
        price_rate = ESTIMATED_PRICE_PER_100G["default"]
        for key, rate in ESTIMATED_PRICE_PER_100G.items():
            if key in name_lower:
                price_rate = rate
                break

        # Rough cost calculation based on weight / standard unit
        item_cost = (scaled_weight / 100.0) * price_rate
        total_cost_inr += max(item_cost, 2.0)  # Minimum base unit ₹2

        scaled_list.append({
            "name_en": ing["name_en"],
            "name_ta": ing["name_ta"],
            "quantity": scaled_qty
        })

    return scaled_list, round(total_cost_inr, 2)


# -----------------------------------------------------------------------------
# 3. NUTRITION & DIABETIC / LOW-GI ESTIMATOR
# -----------------------------------------------------------------------------
def estimate_nutrition(recipe_name: str, servings: int) -> Dict[str, Any]:
    """Computes approximate nutritional metrics and glycemic index advice."""
    name_lower = recipe_name.lower()

    if any(k in name_lower for k in ["sambar", "rasam", "curry", "soup"]):
        cals_per_serving = 160
        protein = 7.5
        carbs = 24.0
        fiber = 6.2
        fat = 4.0
        gi_status = "Low GI (Diabetic Friendly)"
        badge_color = "#2e7d32"
        health_note = "Rich in dietary fiber and pulse protein; causes slow, steady glucose release."
    elif any(k in name_lower for k in ["pongal", "rice", "biryani", "pulao"]):
        cals_per_serving = 340
        protein = 8.0
        carbs = 54.0
        fiber = 2.8
        fat = 11.0
        gi_status = "Moderate GI"
        badge_color = "#f57c00"
        health_note = "High carbohydrate energy. For diabetic diets, pair with double servings of fiber-rich sambar or sautéed greens."
    elif any(k in name_lower for k in ["paneer", "butter"]):
        cals_per_serving = 320
        protein = 14.5
        carbs = 12.0
        fiber = 3.5
        fat = 22.0
        gi_status = "Low GI (Keto / High Protein Friendly)"
        badge_color = "#2e7d32"
        health_note = "High satiety, minimal glycemic impact. Monitor saturated fat intake if managing cholesterol."
    else:
        cals_per_serving = 220
        protein = 8.5
        carbs = 28.0
        fiber = 4.5
        fat = 7.5
        gi_status = "Balanced GI"
        badge_color = "#1976d2"
        health_note = "Well-balanced everyday meal with standard macronutrient distribution."

    return {
        "calories": cals_per_serving,
        "protein": protein,
        "carbs": carbs,
        "fiber": fiber,
        "fat": fat,
        "gi_status": gi_status,
        "badge_color": badge_color,
        "health_note": health_note
    }


# -----------------------------------------------------------------------------
# 4. 1-CLICK WHATSAPP GROCERY LIST GENERATOR
# -----------------------------------------------------------------------------
def generate_whatsapp_grocery_link(recipe_name: str, missing_ingredients: List[Dict[str, str]]) -> str:
    """Generates an immediate WhatsApp deep-link sharing missing ingredients."""
    if not missing_ingredients:
        text = f"🛒 *Meal Matrix Grocery List*\nEverything is available at home for *{recipe_name}*! Ready to cook."
    else:
        lines = [f"🛒 *Meal Matrix - Grocery Checklist for {recipe_name}*"]
        lines.append("Items needed from the store:")
        for idx, item in enumerate(missing_ingredients, start=1):
            lines.append(f"{idx}. {item['name_en']} ({item['name_ta']}) - {item['quantity']}")
        lines.append("\n_Generated via Meal Matrix Assistant_")
        text = "\n".join(lines)

    encoded_text = urllib.parse.quote(text)
    return f"https://api.whatsapp.com/send?text={encoded_text}"


# -----------------------------------------------------------------------------
# 5. CORE TRANSLATION & RECIPE GENERATION
# -----------------------------------------------------------------------------
def translate_to_tamil(text: str) -> str:
    """Translates text or ingredient names to clean Tamil script."""
    try:
        clean = re.sub(r'\(.*?\)', '', text).strip()
        translated = translator.translate(clean)
        return translated if translated else text
    except Exception:
        return text


def get_youtube_embed_url(query: str) -> str:
    """Returns a direct search query for YouTube cooking tutorials."""
    clean_query = urllib.parse.quote(f"{query} recipe cooking tutorial")
    return f"https://www.youtube.com/results?search_query={clean_query}"


def generate_live_recipe(dish_name: str, key_ingredients: List[str] = None) -> Dict[str, Any]:
    """Dynamically constructs a complete structured recipe for ANY dish."""
    clean_name = dish_name.strip().title()
    tamil_name = translate_to_tamil(clean_name)
    dish_id = clean_name.lower().replace(" ", "_")

    is_dessert = any(w in clean_name.lower() for w in ["halwa", "payasam", "cake", "kheer", "sweet", "ladoo"])
    is_rice = any(w in clean_name.lower() for w in ["biryani", "pulao", "rice", "bath", "fried rice"])

    if is_dessert:
        ingredients_raw = [
            ("Main Base Ingredient", "250 grams (1 cup)"),
            ("Sugar / Jaggery", "180 grams (3/4 cup)"),
            ("Pure Desi Ghee", "60 ml (4 tbsp)"),
            ("Cardamom Powder", "3 grams (1/2 tsp fresh)"),
            ("Cashews & Raisins", "30 grams (2 tbsp chopped)")
        ]
        steps = [
            {
                "step_number": 1,
                "title": "Roast Nuts & Base",
                "action_type": "roasting",
                "instruction": f"Heat 30ml ghee in a pan on medium heat. Fry cashews and raisins for 2 minutes until golden brown, set aside. Roast the main base for 5 minutes until fragrant.",
                "timer_seconds": 420,
                "display_timer": "07:00"
            },
            {
                "step_number": 2,
                "title": "Simmer & Sweeten",
                "action_type": "simmering",
                "instruction": f"Add 400ml warm milk or water gradually. Stir continuously for 6 minutes on low heat to avoid lumps. Add sugar/jaggery and mix for 4 minutes until dissolved.",
                "timer_seconds": 600,
                "display_timer": "10:00"
            },
            {
                "step_number": 3,
                "title": "Finish with Cardamom & Ghee",
                "action_type": "mixing",
                "instruction": f"Add remaining ghee and cardamom powder. Stir for 3 minutes until the sweet separates cleanly from the pan. Garnish with roasted nuts and rest for 5 minutes before serving.",
                "timer_seconds": 480,
                "display_timer": "08:00"
            }
        ]
    elif is_rice:
        ingredients_raw = [
            ("Basmati / Ponni Rice", "250 grams (1.25 cups washed)"),
            ("Water / Broth", "500 ml (2 cups)"),
            ("Onions", "150 grams (2 large, sliced)"),
            ("Ginger Garlic Paste", "15 grams (1 tbsp fresh)"),
            ("Whole Spices (Cloves, Cinnamon)", "5 grams (2 each)"),
            ("Cooking Oil or Ghee", "30 ml (2 tbsp)"),
            ("Salt", "6 grams (1 tsp or to taste)")
        ]
        steps = [
            {
                "step_number": 1,
                "title": "Sauté Whole Spices & Onions",
                "action_type": "sauteing",
                "instruction": "Heat 30ml oil/ghee in a cooker. Sauté whole spices for 45 seconds until aromatic. Add sliced onions and ginger garlic paste; sauté for 5 minutes until golden brown.",
                "timer_seconds": 345,
                "display_timer": "05:45"
            },
            {
                "step_number": 2,
                "title": "Add Rice & Measure Liquids",
                "action_type": "boiling",
                "instruction": "Add 250g soaked rice and gently sauté for 60 seconds. Pour 500ml water and add 1 tsp salt. Bring to a rolling boil over medium-high flame for 3 minutes.",
                "timer_seconds": 240,
                "display_timer": "04:00"
            },
            {
                "step_number": 3,
                "title": "Steam & Dum Cooking",
                "action_type": "simmering",
                "instruction": "Cover with lid, reduce flame to the lowest setting, and cook undisturbed for 12 minutes. Turn off heat and rest for 10 minutes before fluffing with a fork.",
                "timer_seconds": 720,
                "display_timer": "12:00"
            }
        ]
    else:
        base_item = key_ingredients[0].title() if key_ingredients else clean_name
        ingredients_raw = [
            (f"{base_item}", "350 grams (fresh, prepared)"),
            ("Onions", "150 grams (2 medium, finely chopped)"),
            ("Tomatoes", "120 grams (2 medium, chopped)"),
            ("Ginger Garlic Paste", "15 grams (1 tbsp)"),
            ("Cooking Oil / Ghee", "25 ml (1.5 tbsp)"),
            ("Turmeric Powder", "2.5 grams (1/2 tsp)"),
            ("Chilli & Coriander Powder", "15 grams (1 tbsp each)"),
            ("Garam Masala", "3 grams (1/2 tsp)"),
            ("Salt", "6 grams (1 tsp or to taste)"),
            ("Water", "250 ml (1 cup)")
        ]
        steps = [
            {
                "step_number": 1,
                "title": "Temper & Sauté Base",
                "action_type": "sauteing",
                "instruction": f"Heat 25ml oil in a heavy pan on medium flame. Sauté onions and ginger garlic paste for 4 minutes until golden brown.",
                "timer_seconds": 240,
                "display_timer": "04:00"
            },
            {
                "step_number": 2,
                "title": "Cook Spices & Tomatoes",
                "action_type": "simmering",
                "instruction": "Add chopped tomatoes, turmeric, chilli powder, and coriander powder. Sauté on medium flame for 6 minutes until oil separates from the gravy edges.",
                "timer_seconds": 360,
                "display_timer": "06:00"
            },
            {
                "step_number": 3,
                "title": f"Cook {clean_name}",
                "action_type": "boiling",
                "instruction": f"Add {base_item}, 250ml water, and 1 tsp salt. Cover with lid and boil on medium heat for 10 minutes until thoroughly cooked.",
                "timer_seconds": 600,
                "display_timer": "10:00"
            },
            {
                "step_number": 4,
                "title": "Garnish & Rest",
                "action_type": "mixing",
                "instruction": "Sprinkle garam masala and fresh coriander leaves. Simmer on low heat for 2 minutes, then turn off heat and rest for 3 minutes before serving.",
                "timer_seconds": 300,
                "display_timer": "05:00"
            }
        ]

    structured_ingredients = []
    for eng_name, qty in ingredients_raw:
        structured_ingredients.append({
            "name_en": eng_name,
            "name_ta": translate_to_tamil(eng_name),
            "quantity": qty
        })

    return {
        "id": dish_id,
        "name": clean_name,
        "tamil_name": tamil_name,
        "cuisine": "Global / Indian Fusion",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "youtube_query": f"{clean_name} recipe step by step",
        "ingredients": structured_ingredients,
        "steps": steps
    }


def search_or_generate_recipe(query: str) -> Dict[str, Any]:
    """Finds recipe in built-in list or generates one live."""
    if not query:
        return BUILTIN_RECIPES[0]

    clean_query = query.strip().lower()
    for r in BUILTIN_RECIPES:
        if clean_query in r["name"].lower() or clean_query in r["tamil_name"].lower():
            return r

    return generate_live_recipe(query)


def match_ingredients(available_ingredients: List[str]) -> List[Dict[str, Any]]:
    """Ranks built-in recipes and synthesizes dishes for ANY typed ingredient."""
    if not available_ingredients:
        return []

    cleaned_pantry = [item.strip().lower() for item in available_ingredients if item.strip()]
    ranked_results = []

    for recipe in BUILTIN_RECIPES:
        matched_items = []
        missing_items = []
        total_ingredients = len(recipe["ingredients"])

        for ing in recipe["ingredients"]:
            ing_en = ing["name_en"].lower()
            ing_ta = ing["name_ta"].lower()
            is_matched = False
            for user_item in cleaned_pantry:
                if user_item in ing_en or user_item in ing_ta:
                    matched_items.append(ing["name_en"])
                    is_matched = True
                    break
            if not is_matched:
                missing_items.append(ing)

        match_count = len(matched_items)
        if match_count > 0:
            match_percentage = round((match_count / total_ingredients) * 100, 1)
            ranked_results.append({
                "recipe": recipe,
                "match_count": match_count,
                "total_count": total_ingredients,
                "match_percentage": match_percentage,
                "matched_ingredients": matched_items,
                "missing_ingredients": missing_items
            })

    # Generate custom dishes for any unusual ingredients
    primary_items = [i.title() for i in cleaned_pantry if len(i) > 2][:3]
    if primary_items:
        primary = primary_items[0]
        secondary = primary_items[1] if len(primary_items) > 1 else "Masala"

        dynamic_dish_names = [
            f"{primary} {secondary} Roast",
            f"Spicy {primary} Gravy",
            f"{primary} Stir Fry",
            f"{primary} Pulao"
        ]

        existing_names = [r["recipe"]["name"].lower() for r in ranked_results]

        for dish_name in dynamic_dish_names:
            if dish_name.lower() not in existing_names:
                gen_rec = generate_live_recipe(dish_name, key_ingredients=cleaned_pantry)
                ranked_results.append({
                    "recipe": gen_rec,
                    "match_count": len(cleaned_pantry),
                    "total_count": len(gen_rec["ingredients"]),
                    "match_percentage": min(100.0, round((len(cleaned_pantry) / len(gen_rec["ingredients"])) * 100 + 40, 1)),
                    "matched_ingredients": [item.title() for item in cleaned_pantry],
                    "missing_ingredients": gen_rec["ingredients"][len(cleaned_pantry):]
                })

    ranked_results.sort(key=lambda x: (x["match_count"], x["match_percentage"]), reverse=True)
    return ranked_results


def get_all_unique_ingredients() -> List[str]:
    unique = set()
    for recipe in BUILTIN_RECIPES:
        for ing in recipe["ingredients"]:
            label = f"{ing['name_en'].split('(')[0].strip()} ({ing['name_ta']})"
            unique.add(label)
    return sorted(list(unique))
