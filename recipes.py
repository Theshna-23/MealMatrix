"""
recipes.py - Recipe Database with High-Resolution Dish Photography
"""

BUILTIN_RECIPES = [
    {
        "id": "sambar",
        "name": "South Indian Sambar",
        "tamil_name": "சாம்பார்",
        "cuisine": "South Indian Traditional",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=900&auto=format&fit=crop&q=80",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "youtube_query": "South Indian sambar recipe step by step",
        "ingredients": [
            {"name_en": "Toor Dal (Split Pigeon Peas)", "name_ta": "துவரம் பருப்பு", "quantity": "100 grams (1/2 cup)"},
            {"name_en": "Water", "name_ta": "தண்ணீர்", "quantity": "750 ml (3 cups)"},
            {"name_en": "Turmeric Powder", "name_ta": "மஞ்சள் தூள்", "quantity": "2.5 grams (1/2 tsp)"},
            {"name_en": "Shallots (Small Onions)", "name_ta": "சின்ன வெங்காயம்", "quantity": "100 grams (10-12 peeled)"},
            {"name_en": "Tomatoes", "name_ta": "தக்காளி", "quantity": "120 grams (1 medium, chopped)"},
            {"name_en": "Drumstick / Mixed Vegetables", "name_ta": "முருங்கைக்காய்", "quantity": "150 grams (1 cup chopped)"},
            {"name_en": "Tamarind Pulp", "name_ta": "புளி சாறு", "quantity": "30 ml (2 tbsp soaked in warm water)"},
            {"name_en": "Sambar Powder", "name_ta": "சாம்பார் பொடி", "quantity": "15 grams (1.5 tbsp)"},
            {"name_en": "Mustard Seeds", "name_ta": "கடுகு", "quantity": "2.5 grams (1/2 tsp)"},
            {"name_en": "Curry Leaves", "name_ta": "கறிவேப்பிலை", "quantity": "10 leaves (1 sprig)"},
            {"name_en": "Gingelly Oil / Ghee", "name_ta": "நல்லெண்ணெய் / நெய்", "quantity": "15 ml (1 tbsp)"},
            {"name_en": "Salt", "name_ta": "உப்பு", "quantity": "6 grams (1 tsp or to taste)"}
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Pressure Cook Dal",
                "action_type": "boiling",
                "instruction": "Rinse 100g toor dal, add 500ml water and 1/2 tsp turmeric powder. Pressure cook on medium flame for 4 whistles (approx. 10 minutes), then let pressure release naturally.",
                "timer_seconds": 600,
                "display_timer": "10:00"
            },
            {
                "step_number": 2,
                "title": "Sauté Aromatics & Vegetables",
                "action_type": "sauteing",
                "instruction": "Heat 15ml oil in a pot over medium flame. Splutter 1/2 tsp mustard seeds and curry leaves for 30 seconds. Add shallots and chopped tomatoes; sauté for 3 minutes until soft.",
                "timer_seconds": 210,
                "display_timer": "03:30"
            },
            {
                "step_number": 3,
                "title": "Boil Vegetables with Tamarind",
                "action_type": "simmering",
                "instruction": "Add vegetables, sambar powder, 1 tsp salt, and 250ml water. Boil for 8 minutes until vegetables are tender, then pour in 30ml tamarind extract.",
                "timer_seconds": 480,
                "display_timer": "08:00"
            },
            {
                "step_number": 4,
                "title": "Combine Dal & Simmer",
                "action_type": "mixing",
                "instruction": "Pour the mashed cooked dal into the boiling vegetable gravy. Stir continuously for 60 seconds and simmer on low-medium flame for 5 minutes.",
                "timer_seconds": 300,
                "display_timer": "05:00"
            }
        ]
    },
    {
        "id": "ven_pongal",
        "name": "Ven Pongal (Ghee Khichdi)",
        "tamil_name": "வெண் பொங்கல்",
        "cuisine": "South Indian Breakfast",
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=900&auto=format&fit=crop&q=80",
        "servings": 3,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "youtube_query": "Ven pongal recipe hotel style",
        "ingredients": [
            {"name_en": "Raw Rice (Ponni/Sona Masoori)", "name_ta": "பச்சரிசி", "quantity": "150 grams (3/4 cup)"},
            {"name_en": "Yellow Moong Dal", "name_ta": "பாசிப்பருப்பு", "quantity": "50 grams (1/4 cup)"},
            {"name_en": "Water", "name_ta": "தண்ணீர்", "quantity": "1000 ml (4 cups)"},
            {"name_en": "Pure Desi Ghee", "name_ta": "நெய்", "quantity": "45 ml (3 tbsp)"},
            {"name_en": "Black Peppercorns", "name_ta": "மிளகு", "quantity": "4 grams (1 tsp, crushed)"},
            {"name_en": "Cumin Seeds", "name_ta": "சீரகம்", "quantity": "4 grams (1 tsp)"},
            {"name_en": "Ginger", "name_ta": "இஞ்சி", "quantity": "10 grams (1 tbsp finely chopped)"},
            {"name_en": "Curry Leaves", "name_ta": "கறிவேப்பிலை", "quantity": "8 to 10 leaves"},
            {"name_en": "Cashew Nuts", "name_ta": "முந்திரி பருப்பு", "quantity": "25 grams (10-12 halves)"},
            {"name_en": "Salt", "name_ta": "உப்பு", "quantity": "5 grams (1 tsp)"}
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Dry Roast Dal",
                "action_type": "roasting",
                "instruction": "Dry roast 50g yellow moong dal in a pan on medium-low heat for 3 minutes until aromatic and lightly golden.",
                "timer_seconds": 180,
                "display_timer": "03:00"
            },
            {
                "step_number": 2,
                "title": "Pressure Cook Rice & Dal",
                "action_type": "boiling",
                "instruction": "Combine roasted dal with 150g washed rice, 1000ml water, and 1 tsp salt. Pressure cook on high for 4 whistles, then simmer on low for 5 minutes (12 minutes total).",
                "timer_seconds": 720,
                "display_timer": "12:00"
            },
            {
                "step_number": 3,
                "title": "Temper Spices in Ghee",
                "action_type": "sauteing",
                "instruction": "Heat 45ml ghee in a small pan. Fry cashews for 2 minutes until golden brown. Add cumin, crushed black pepper, chopped ginger, and curry leaves; sizzle for 45 seconds.",
                "timer_seconds": 165,
                "display_timer": "02:45"
            },
            {
                "step_number": 4,
                "title": "Combine & Rest",
                "action_type": "mixing",
                "instruction": "Pour the sizzling ghee tempering over the cooked, mashed rice-dal mix. Mix thoroughly for 60 seconds, cover, and rest for 3 minutes before serving.",
                "timer_seconds": 240,
                "display_timer": "04:00"
            }
        ]
    },
    {
        "id": "paneer_butter_masala",
        "name": "Paneer Butter Masala",
        "tamil_name": "பன்னீர் பட்டர் மசாலா",
        "cuisine": "North Indian Delicacy",
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=900&auto=format&fit=crop&q=80",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 20,
        "youtube_query": "Restaurant style paneer butter masala recipe",
        "ingredients": [
            {"name_en": "Paneer (Cottage Cheese)", "name_ta": "பன்னீர்", "quantity": "250 grams (cubed)"},
            {"name_en": "Butter", "name_ta": "வெண்ணெய்", "quantity": "40 grams (2.5 tbsp)"},
            {"name_en": "Tomatoes", "name_ta": "தக்காளி", "quantity": "300 grams (4 ripe, puréed)"},
            {"name_en": "Onion", "name_ta": "வெங்காயம்", "quantity": "120 grams (1 large, chopped)"},
            {"name_en": "Cashews", "name_ta": "முந்திரி பருப்பு", "quantity": "20 grams (12-15 soaked & ground)"},
            {"name_en": "Ginger Garlic Paste", "name_ta": "இஞ்சி பூண்டு விழுது", "quantity": "15 grams (1 tbsp)"},
            {"name_en": "Fresh Cream", "name_ta": "பிரெஷ் கிரீம்", "quantity": "30 ml (2 tbsp)"},
            {"name_en": "Kasuri Methi", "name_ta": "கசூரி மேத்தி", "quantity": "3 grams (1 tsp crushed)"},
            {"name_en": "Garam Masala", "name_ta": "கரம் மசாலா", "quantity": "5 grams (1 tsp)"},
            {"name_en": "Kashmiri Chilli Powder", "name_ta": "காஷ்மீரி மிளகாய் தூள்", "quantity": "7 grams (1.5 tsp)"},
            {"name_en": "Salt", "name_ta": "உப்பு", "quantity": "5 grams (1 tsp)"}
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Prepare Makhani Gravy Base",
                "action_type": "sauteing",
                "instruction": "Melt 20g butter in a pan over medium heat. Sauté onions and ginger garlic paste for 4 minutes until raw aroma disappears. Add tomato purée and cook for 6 minutes.",
                "timer_seconds": 600,
                "display_timer": "10:00"
            },
            {
                "step_number": 2,
                "title": "Spice and Add Cashew Paste",
                "action_type": "simmering",
                "instruction": "Stir in chilli powder, garam masala, salt, and smooth cashew paste. Add 100ml water and simmer on low-medium flame for 5 minutes until gravy becomes glossy.",
                "timer_seconds": 300,
                "display_timer": "05:00"
            },
            {
                "step_number": 3,
                "title": "Add Paneer & Cream",
                "action_type": "mixing",
                "instruction": "Gently add paneer cubes and remaining 20g butter. Simmer for 3 minutes on low flame so paneer stays soft. Finish with fresh cream and crushed kasuri methi.",
                "timer_seconds": 180,
                "display_timer": "03:00"
            }
        ]
    }
]

def get_all_recipes():
    return BUILTIN_RECIPES

def get_recipe_by_id(recipe_id: str):
    for r in BUILTIN_RECIPES:
        if r["id"] == recipe_id:
            return r
    return None
