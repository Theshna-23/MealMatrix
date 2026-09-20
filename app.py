"""
=============================================================================
MEAL MATRIX - SMART CULINARY STUDIO WITH 5 INNOVATIVE FEATURES:
1. Smart Recipe Scaler & Cost Estimator
2. Nutrition & Diabetic / Low-GI Health Mode
3. Intelligent Culinary Substitute Engine
4. 1-Click WhatsApp Missing-Ingredients List
5. Hands-Free Audio Voice Assistant & Kitchen Mode
=============================================================================
Run using:
    streamlit run app.py
=============================================================================
"""

import os
import tempfile
import streamlit as st
from gtts import gTTS

from recipes import get_all_recipes, get_recipe_by_id
from utils import (
    search_or_generate_recipe,
    match_ingredients,
    get_all_unique_ingredients,
    get_youtube_embed_url,
    calculate_cost_and_scaled_ingredients,
    estimate_nutrition,
    find_ingredient_substitute,
    generate_whatsapp_grocery_link
)
from video_generator import create_recipe_video

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Meal Matrix | Next-Gen Cooking Studio",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System
st.markdown("""
    <style>
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ff5722;
        margin-bottom: 0.1rem;
    }
    .badge-tamil {
        background-color: #fff3e0;
        color: #e65100;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 1.15rem;
        font-weight: bold;
    }
    .nutrition-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .timer-pill {
        background-color: #2e7d32;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .cost-badge {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Reusable Rich Recipe Viewer (Features 1, 2, 4, 5)
# -----------------------------------------------------------------------------
def render_full_recipe_card(recipe: dict, key_prefix: str = "main"):
    """
    Renders the complete recipe view with:
    - Interactive Scaler & Cost Estimator
    - Nutrition & Diabetic Health Profile
    - Bilingual exact ingredients
    - Culinary Substitute Swapper
    - Timed cooking instructions
    - Hands-Free Audio Voice Assistant
    """
    st.markdown(
        f"## {recipe['name']} <span class='badge-tamil'>{recipe['tamil_name']}</span>",
        unsafe_allow_html=True
    )

    # 1. SMART RECIPE SCALER & COST ESTIMATOR
    st.markdown("#### ⚖️ 1. Smart Scaler & Budget Estimator")
    base_servings = recipe.get("servings", 4)

    col_scale, col_cost, col_yt = st.columns([2, 2, 2])
    with col_scale:
        target_servings = st.slider(
            "Select Portions / Servings to Cook:",
            min_value=1,
            max_value=20,
            value=base_servings,
            key=f"{key_prefix}_servings_slider"
        )
    
    scaled_ingredients, estimated_cost_inr = calculate_cost_and_scaled_ingredients(
        recipe["ingredients"],
        base_servings=base_servings,
        target_servings=target_servings
    )

    with col_cost:
        st.metric(
            label=f"Estimated Grocery Cost ({target_servings} servings)",
            value=f"₹{estimated_cost_inr:.0f} INR",
            delta=f"~₹{estimated_cost_inr/target_servings:.1f} / person"
        )

    with col_yt:
        yt_link = get_youtube_embed_url(recipe.get("youtube_query", recipe["name"]))
        st.write(" ")
        st.link_button("▶️ Watch YouTube Cooking Guide", yt_link, use_container_width=True)

    # 2. NUTRITION & DIABETIC / LOW-GI MODE
    st.markdown("#### 🥗 2. Nutrition & Diabetic Health Mode")
    nutri = estimate_nutrition(recipe["name"], target_servings)
    
    with st.container():
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.metric("Calories", f"{nutri['calories']} kcal")
        n2.metric("Protein", f"{nutri['protein']} g")
        n3.metric("Carbohydrates", f"{nutri['carbs']} g")
        n4.metric("Dietary Fiber", f"{nutri['fiber']} g")
        n5.metric("Healthy Fats", f"{nutri['fat']} g")
        
        st.markdown(
            f"**Glycemic Assessment:** <span style='background-color:{nutri['badge_color']}; color:white; padding:3px 8px; border-radius:4px;'>{nutri['gi_status']}</span> — *{nutri['health_note']}*",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 3. EXACT INGREDIENTS LIST
    st.markdown("#### 🛒 3. Ingredients (Scaled to Exact Grams / ml)")
    half = (len(scaled_ingredients) + 1) // 2
    c1, c2 = st.columns(2)
    with c1:
        for ing in scaled_ingredients[:half]:
            st.markdown(f"- **{ing['name_en']}** (`{ing['name_ta']}`): **{ing['quantity']}**")
    with c2:
        for ing in scaled_ingredients[half:]:
            st.markdown(f"- **{ing['name_en']}** (`{ing['name_ta']}`): **{ing['quantity']}**")

    # 4. INTELLIGENT CULINARY SUBSTITUTE ENGINE
    with st.expander("🔄 4. Missing an Ingredient? Find Smart Culinary Substitutes"):
        st.caption("Don't have tamarind, ghee, paneer, curd, or tomatoes? Select below for instant culinary swaps:")
        ingredient_names = [i["name_en"] for i in scaled_ingredients]
        chosen_missing = st.selectbox(
            "Select an ingredient you are missing:",
            options=ingredient_names,
            key=f"{key_prefix}_sub_select"
        )
        if chosen_missing:
            sub_info = find_ingredient_substitute(chosen_missing)
            st.info(f"**Flavor Profile:** {sub_info['taste_profile']}")
            st.write("**Recommended Alternatives:**")
            for alt in sub_info["alternatives"]:
                st.markdown(f"• {alt}")

    st.markdown("---")

    # 5. STEP-BY-STEP TIMED METHOD + HANDS-FREE AUDIO ASSISTANT
    st.markdown("#### 👨‍🍳 5. Step-by-Step Method & Hands-Free Audio Assistant")
    
    # Hands-Free Audio Guide Trigger
    with st.expander("🎙️ Open Hands-Free Audio Voice Assistant (Kitchen Mode)"):
        st.caption("Listen to spoken step-by-step guidance while your hands are busy cooking.")
        for s in recipe["steps"]:
            step_col, audio_col = st.columns([3, 2])
            with step_col:
                st.write(f"**Step {s['step_number']}: {s['title']}** (⏳ {s['display_timer']})")
                st.caption(s["instruction"])
            with audio_col:
                if st.button(f"🔊 Read Step {s['step_number']} Aloud", key=f"{key_prefix}_audio_{s['step_number']}"):
                    tts = gTTS(text=f"Step {s['step_number']}: {s['title']}. {s['instruction']}", lang='en', slow=False)
                    temp_aud = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                    tts.save(temp_aud.name)
                    st.audio(temp_aud.name, format="audio/mp3")

    for s in recipe["steps"]:
        with st.container():
            st.markdown(
                f"##### Step {s['step_number']}: {s['title']} &nbsp;&nbsp;<span class='timer-pill'>⏳ {s['display_timer']}</span>",
                unsafe_allow_html=True
            )
            st.write(s["instruction"])
            st.divider()


# -----------------------------------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400&q=80", caption="Meal Matrix Studio")
st.sidebar.title("Meal Matrix Menu")
selected_feature = st.sidebar.radio(
    "Choose Mode",
    [
        "FEATURE 1: Search Any Dish (Unlimited)",
        "FEATURE 2: What Can I Cook? (Pantry + WhatsApp)",
        "FEATURE 3: Real Video Cooking Guide"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Meal Matrix • College Project Submission • 5 Intelligent Systems")


# -----------------------------------------------------------------------------
# FEATURE 1: Unlimited Dishes + All 5 Features
# -----------------------------------------------------------------------------
if selected_feature == "FEATURE 1: Search Any Dish (Unlimited)":
    st.markdown("<div class='hero-title'>Global Recipe Explorer</div>", unsafe_allow_html=True)
    st.caption("Search ANY dish in the world. Includes Scaler, Cost Estimator, Nutrition Mode, Substitute Swapper, and Audio Voice Guidance.")

    dish_query = st.text_input("Enter any dish name:", value="South Indian Sambar")

    if st.button("Get Complete Recipe", type="primary"):
        with st.spinner(f"Preparing recipe with nutrition and Tamil translation for '{dish_query}'..."):
            recipe_data = search_or_generate_recipe(dish_query)
            st.session_state["current_recipe"] = recipe_data

    if "current_recipe" in st.session_state:
        render_full_recipe_card(st.session_state["current_recipe"], key_prefix="f1")


# -----------------------------------------------------------------------------
# FEATURE 2: Universal What Can I Cook? + 1-Click WhatsApp Shopping
# -----------------------------------------------------------------------------
elif selected_feature == "FEATURE 2: What Can I Cook? (Pantry + WhatsApp)":
    st.markdown("<div class='hero-title'>Universal Pantry Matcher & WhatsApp Grocery</div>", unsafe_allow_html=True)
    st.caption("Type ANY ingredients sitting in your kitchen. The system displays all dishes you can make and generates a 1-Click WhatsApp shopping list for missing ingredients.")

    all_ingredients = get_all_unique_ingredients()
    selected_pantry = st.multiselect(
        "Pick common pantry staples:",
        options=all_ingredients,
        default=[]
    )

    custom_entry = st.text_input(
        "👉 Or type ANY custom ingredients (separated by commas):",
        value="Chicken, Pepper, Garlic",
        help="Type anything! E.g. Egg, Onion OR Mushroom, Garlic OR Paneer, Butter"
    )

    ingredients_to_search = list(selected_pantry)
    if custom_entry.strip():
        extra_items = [x.strip() for x in custom_entry.split(",") if x.strip()]
        ingredients_to_search.extend(extra_items)

    if st.button("Discover All Dishes I Can Cook", type="primary"):
        if not ingredients_to_search:
            st.error("Please pick or type at least one ingredient.")
        else:
            with st.spinner("Finding all matching dishes and computing missing ingredients..."):
                clean_tokens = [item.split("(")[0].strip() for item in ingredients_to_search]
                results = match_ingredients(clean_tokens)

                st.success(f"Discovered {len(results)} dishes you can cook with your ingredients!")
                
                for idx, match in enumerate(results, start=1):
                    rec = match["recipe"]
                    missing = match.get("missing_ingredients", [])

                    with st.expander(
                        f"Dish #{idx}: {rec['name']} ({rec['tamil_name']}) — {match['match_percentage']}% Match",
                        expanded=(idx == 1)
                    ):
                        st.markdown(f"**✅ Matched from your kitchen:** {', '.join(match['matched_ingredients'])}")
                        
                        # 1-CLICK WHATSAPP GROCERY FEATURE
                        if missing:
                            wa_url = generate_whatsapp_grocery_link(rec["name"], missing)
                            st.markdown(
                                f"**⚠️ Missing ({len(missing)} items):** {', '.join([m['name_en'] for m in missing])}"
                            )
                            st.link_button(
                                label="📲 Send Missing Items to WhatsApp Grocery List",
                                url=wa_url,
                                use_container_width=True
                            )
                        else:
                            st.success("🎉 You have 100% of the ingredients required for this dish!")

                        st.markdown("---")
                        render_full_recipe_card(rec, key_prefix=f"pantry_{idx}")


# -----------------------------------------------------------------------------
# FEATURE 3: Real Video Cooking Guide
# -----------------------------------------------------------------------------
elif selected_feature == "FEATURE 3: Real Video Cooking Guide":
    st.markdown("<div class='hero-title'>Real Video Cooking Guide</div>", unsafe_allow_html=True)
    st.caption("Stitches real video footage of cooking actions (sautéing, boiling, simmering) synchronized with gTTS voice narration into an MP4.")

    target_dish = st.text_input("Enter dish for video generation:", value="South Indian Sambar")
    recipe_for_video = search_or_generate_recipe(target_dish)

    st.write(f"Ready to synthesize a **{len(recipe_for_video['steps'])}-step real video guide** for **{recipe_for_video['name']}**.")

    col_btn, col_yt = st.columns([2, 2])
    with col_btn:
        generate_clicked = st.button("🎬 Generate Real Action Video (.mp4)", type="primary")
    with col_yt:
        yt_url = get_youtube_embed_url(recipe_for_video["name"])
        st.link_button("📺 Open Direct YouTube Video Guide", yt_url)

    if generate_clicked:
        with st.spinner("Downloading real culinary video clips, generating voiceover narration, and rendering MP4..."):
            try:
                temp_output = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
                temp_output.close()

                video_path = create_recipe_video(recipe_for_video, temp_output.name)

                st.success("Real cooking video successfully rendered!")

                with open(video_path, "rb") as vf:
                    video_bytes = vf.read()
                    st.video(video_bytes)

                st.download_button(
                    label="💾 Download Cooking Video (.mp4)",
                    data=video_bytes,
                    file_name=f"{recipe_for_video['id']}_guide.mp4",
                    mime="video/mp4"
                )

            except Exception as e:
                st.error(f"Video synthesis notice: {str(e)}")
                st.info("Ensure your internet connection is active so real stock video clips and voiceover can download smoothly.")
