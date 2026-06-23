# main.py (cleaned + fixed hero + updated use_container_width)
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import base64
import io
import json
import streamlit.components.v1 as components

# -------------------- Helpers --------------------
@st.cache_data
def load_data(path="dataset/Airbnb_Cleaned.csv"):
    """
    Load CSV safely. If parse_dates columns don't exist, load without parse_dates.
    """
    try:
        df = pd.read_csv(
            path,
            parse_dates=["first_review", "host_since", "last_review", "available_date"],
            low_memory=False,
        )
    except Exception:
        df = pd.read_csv(path, low_memory=False)
    return df


def short_name_from_email(email):
    if pd.isna(email) or "@" not in str(email):
        return str(email)
    return email.split("@")[0].replace(".", " ").title()


def img_file_to_base64(path):
    """Read image file and return base64 string (utf-8)."""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def gather_local_images(img_dir="images", bases=None, limit=10):
    """
    Return list of image paths (local or remote fallback).
    - bases: list of basenames to prioritize, e.g. ["image1","image2","image3"]
    - if bases not found, will list files from folder (sorted)
    """
    images = []

    if bases:
        for base in bases:
            for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                p = os.path.join(img_dir, base + ext)
                if os.path.exists(p):
                    images.append(p)
                    break

    # if still empty, take any images from folder
    if (not images) and os.path.exists(img_dir):
        for fname in sorted(os.listdir(img_dir)):
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
                images.append(os.path.join(img_dir, fname))
                if len(images) >= limit:
                    break

    return images


# -------------------- App config --------------------#
st.set_page_config(page_title="Personalized Stay — Friendly Travel", layout="wide")

# -------------------- Large fixed navbar with logo (place right after st.set_page_config(...)) --------------------
logo_path = "images/logo.png"
if os.path.exists(logo_path):
    img_b64 = img_file_to_base64(logo_path)
else:
    img_b64 = ""  # empty fallback

# Navbar sizes (adjust to taste)
NAV_HEIGHT_PX = 92
NAV_HEIGHT_MOBILE = 72

st.markdown(
    f"""
    <style>
    /* push app down so navbar doesn't overlap content */
    .stApp {{
        padding-top: {NAV_HEIGHT_PX}px;
    }}

    /* navbar */
    .top-navbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: {NAV_HEIGHT_PX}px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 80px;
        z-index: 2147483647;
        backdrop-filter: blur(6px);
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.96));
        border-bottom: 1px solid rgba(18,18,18,0.06);
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    }}

    .nav-left {{
        display: flex;
        align-items: center;
        gap: 14px;
        min-width: 0;
        justify-content: flex-start; 
    }}

    .brand-logo {{
        height: calc({NAV_HEIGHT_PX}px - 30px);
        width: auto;
        display: block;
    }}

    .brand-title {{
        font-size: 20px;
        font-weight: 800;
        color: #0f1720;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .nav-links {{
        display: flex;
        gap: 20px;
        align-items: center;
        font-weight: 700;
    }}
    .nav-link {{
        text-decoration: none;
        color: #0f1720;
        padding: 8px 10px;
        border-radius: 8px;
        transition: all .18s ease;
        font-size: 15px;
    }}
    .nav-link:hover {{
        transform: translateY(-2px);
        background: rgba(148,68,237,0.06);
        color: #9444ED;
    }}

    .nav-actions {{
        display: flex;
        gap: 12px;
        align-items: center;
    }}
    .btn {{
        display: inline-block;
        padding: 9px 14px;
        border-radius: 10px;
        font-weight: 800;
        text-decoration: none;
        font-size: 14px;
    }}
    .btn-ghost {{
        background: transparent;
        color: #0f1720;
        border: 1px solid rgba(18,18,18,0.08);
    }}
    .btn-primary {{
        background: linear-gradient(90deg,#9444ED,#FF914D);
        color: #fff;
        box-shadow: 0 8px 22px rgba(148,68,237,0.12);
    }}

    .hamburger {{
        display: none;
        width: 44px;
        height: 44px;
        justify-content: center;
        align-items: center;
        border-radius: 8px;
        cursor: pointer;
        border: 1px solid rgba(18,18,18,0.06);
        background: rgba(255,255,255,0.9);
    }}

    /* mobile responsive */
    @media (max-width: 920px) {{
        .nav-links {{
            display: none;
        }}
        .hamburger {{
            display: flex;
        }}
        .stApp {{
            padding-top: {NAV_HEIGHT_MOBILE}px;
        }}
        .brand-title {{
            display: none;
        }}
        .brand-logo {{
            height: calc({NAV_HEIGHT_MOBILE}px - 20px);
        }}
    }}

    /* mobile menu */
    .mobile-menu {{
        display: none;
        position: fixed;
        top: {NAV_HEIGHT_PX}px;
        left: 0;
        right: 0;
        background: #ffffff;
        z-index: 2147483646;
        border-bottom: 1px solid rgba(18,18,18,0.04);
        box-shadow: 0 14px 40px rgba(0,0,0,0.06);
        padding: 12px 18px;
    }}
    .mobile-menu.open {{
        display: block;
    }}
    .mobile-menu a {{
        display: block;
        padding: 10px 6px;
        text-decoration: none;
        color: #0f1720;
        font-weight: 800;
        border-radius: 6px;
    }}
    .mobile-menu a + a {{
        margin-top: 8px;
    }}
    </style>

    <header class="top-navbar" role="banner" aria-label="Top navigation">
      <div class="nav-left">
        <a href="#" style="display:flex;align-items:center;gap:12px;text-decoration:none;">
          <img class="brand-logo" src="data:image/png;base64,{img_b64}" alt="logo" />
          <span class="brand-title">Personalized Stay</span>
        </a>
      </div>

      <div class="nav-actions">
        <div class="hamburger" id="hamburger" aria-label="Open menu" title="Open menu">
          <svg width="18" height="14" viewBox="0 0 18 14" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <rect y="1" width="18" height="2" rx="1" fill="#111827"></rect>
            <rect y="6" width="18" height="2" rx="1" fill="#111827"></rect>
            <rect y="11" width="18" height="2" rx="1" fill="#111827"></rect>
          </svg>
        </div>
      </div>
    </header>

    <div class="mobile-menu" id="mobileMenu" aria-hidden="true">
      <div style="height:8px;"></div>
      <a href="#" style="color:#9444ED;font-weight:900;">Sign In / Create</a>
    </div>

    <script>
    (function() {{
      const hamburger = document.getElementById('hamburger');
      const mobileMenu = document.getElementById('mobileMenu');
      let open = false;
      hamburger && hamburger.addEventListener('click', function(e) {{
        open = !open;
        if (open) {{
          mobileMenu.classList.add('open');
          mobileMenu.setAttribute('aria-hidden', 'false');
        }} else {{
          mobileMenu.classList.remove('open');
          mobileMenu.setAttribute('aria-hidden', 'true');
        }}
      }});

      document.addEventListener('click', function(ev) {{
        if (!hamburger.contains(ev.target) && !mobileMenu.contains(ev.target)) {{
          mobileMenu.classList.remove('open');
          mobileMenu.setAttribute('aria-hidden', 'true');
          open = false;
        }}
      }});
    }})();
    </script>
    """,
    unsafe_allow_html=True,
)
# -------------------- Load dataset --------------------
with st.spinner("Loading dataset..."):
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Dataset file not found at dataset/Airbnb_Cleaned.csv — showing empty sample.")
        df = pd.DataFrame(
            {
                "id": range(1, 11),
                "name": [f"Hotel {i}" for i in range(1, 11)],
                "thumbnail_url": [None, *[f"https://picsum.photos/seed/{i}/600/400" for i in range(1, 10)]],
                "review_scores_rating": np.random.randint(60, 100, 10),
                "number_of_reviews": np.random.randint(0, 500, 10),
                "was_price": [None] + list(np.random.randint(50, 500, 9)),
                "log_price": np.random.uniform(30, 400, 10),
                "country": ["USA", "Indonesia", "USA", "France", "USA", "Japan", "Indonesia", "USA", "Spain", "USA"],
                "property_type": ["Apartment", "House", "Apartment", "B&B", "Apartment", "Villa", "Apartment", "Hostel", "House", "Resort"],
            }
        )

# -------------------- Session state defaults --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_country" not in st.session_state:
    st.session_state.user_country = None
if "_slider_index" not in st.session_state:
    st.session_state["_slider_index"] = 0
if "image_pointer" not in st.session_state:
    st.session_state.image_pointer = 0

# -------------------- Login placeholder --------------------
if not st.session_state.logged_in:
    login_placeholder = st.empty()
    with login_placeholder.container():
        st.markdown("### 👋 Welcome to **Personalized Stay**")
        st.info("Make every trip feel like coming home 🌍")
        st.write("Create an account or sign in to get recommendations tailored for you.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌐 Continue with Google"):
                st.session_state.user_email = "guest_google@example.com"
                st.session_state.logged_in = True
                st.success("Signed in as guest_google@example.com")
                
        with col2:
            if st.button("📘 Continue with Facebook"):
                st.session_state.user_email = "guest_facebook@example.com"
                st.session_state.logged_in = True
                st.success("Signed in as guest_facebook@example.com")
                

        st.markdown("---")
        st.write("**Or sign in / create with email**")

        with st.form("email_form"):
            email = st.text_input("Email", placeholder="name@email.com")
            countries = sorted(df["country"].dropna().unique()) if "country" in df.columns else ["Indonesia"]
            country = st.selectbox("Country", options=countries)
            st.write("_with phone number_")
            submit = st.form_submit_button("Sign in / Create")
            if submit:
                st.session_state.user_email = email if email else "guest_user@example.com"
                st.session_state.user_country = country
                st.session_state.logged_in = True
                st.success(f"Welcome, {short_name_from_email(st.session_state.user_email)}!")
                login_placeholder.empty()

if not st.session_state.logged_in:
    st.stop()

# -------------------- Main header --------------------
user_name = short_name_from_email(st.session_state.user_email)
user_country = st.session_state.user_country if st.session_state.user_country else "your country"

# Add some left padding so header content doesn't visually butt up to fixed logo
st.markdown('<div style="padding-left:100px;">', unsafe_allow_html=True)
st.markdown(f"# Personalized Stay — Welcome back, {user_name} 👋")
st.markdown(f"### Planning another trip to **{user_country}** or international?")
st.markdown("</div>", unsafe_allow_html=True)

st.write("\n")

# -------------------- Fixed-height Hero / Image Slider --------------------
local_images = gather_local_images(img_dir="images", bases=["image1", "image2", "image3"], limit=12)

# Build src list (local -> data URI, remote as-is)
src_list = []
for p in local_images:
    try:
        if isinstance(p, str) and p.startswith("http"):
            src_list.append(p)
        else:
            ext = os.path.splitext(p)[1].lower()
            mime = "image/jpeg"
            if ext == ".png":
                mime = "image/png"
            elif ext == ".webp":
                mime = "image/webp"
            elif ext == ".gif":
                mime = "image/gif"
            b64 = img_file_to_base64(p)
            src_list.append(f"data:{mime};base64,{b64}")
    except Exception:
        src_list.append("https://picsum.photos/1920/1080")

if not src_list:
    src_list = ["https://picsum.photos/1920/1080"]

# Fixed hero height in pixels to keep iframe stable and avoid whitespace/shape shifts on zoom.
HERO_HEIGHT_PX = 600  # adjust if desired (desktop comfortable default)

images_js_array = json.dumps(src_list)

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1.0" />
<style>
  html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    background: transparent;
  }}
  .full-bleed {{
    position: relative;
    width: 100%;
    height: {HERO_HEIGHT_PX}px;
    max-height: {HERO_HEIGHT_PX}px;
    min-height: {HERO_HEIGHT_PX}px;
    overflow: hidden;
    background-color: #000;
  }}
  .full-bleed img {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center center;
    transition: opacity 0.8s ease-in-out, transform 0.8s ease-in-out;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    will-change: opacity;
  }}
  img {{ display: block; }}
  @media (max-width: 600px) {{
    .full-bleed {{
      height: 420px;
      max-height: 420px;
      min-height: 420px;
    }}
  }}
</style>
</head>
<body>
  <div class="full-bleed" aria-hidden="true">
    <img id="img1" src="{src_list[0]}" style="opacity:1;" alt="featured image 1" />
    <img id="img2" src="{src_list[0]}" style="opacity:0;" alt="featured image 2" />
  </div>

  <script>
    const images = {images_js_array};
    let idx = 0;
    let showingFirst = true;
    const img1 = document.getElementById('img1');
    const img2 = document.getElementById('img2');

    images.forEach(u => {{
      const i = new Image();
      i.src = u;
    }});

    if (images.length === 0) {{
      images.push("https://picsum.photos/1920/1080");
    }}

    function showNext() {{
      idx = (idx + 1) % images.length;
      const next = images[idx];
      if (showingFirst) {{
        img2.src = next;
        img2.style.opacity = 1;
        img1.style.opacity = 0;
      }} else {{
        img1.src = next;
        img1.style.opacity = 1;
        img2.style.opacity = 0;
      }}
      showingFirst = !showingFirst;
    }}

    const INTERVAL_MS = 10000;
    let rotation = setInterval(showNext, INTERVAL_MS);

    document.addEventListener('visibilitychange', function() {{
      if (document.hidden) {{
        clearInterval(rotation);
      }} else {{
        rotation = setInterval(showNext, INTERVAL_MS);
      }}
    }});
  </script>
</body>
</html>
"""

components.html(html, height=HERO_HEIGHT_PX, scrolling=False)
st.markdown("---")

# -------------------- Filter Card Section --------------------
st.markdown("### 🏠 Find Your Perfect Stay")

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("📍 **Location**")
        location = st.text_input("Around me", value="Around me", label_visibility="collapsed")

    with col2:
        st.markdown("📅 **Date**")
        selected_date = st.date_input("Select Date", value=pd.Timestamp("2025-10-25"), label_visibility="collapsed")

    with col3:
        st.markdown("🌙 **Night Stay**")
        night_stay = st.selectbox("Night Stay", list(range(1, 31)), index=2, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    # Gunakan nilai minimum dari data agar dropdown dinamis
    def get_unique_int_values(series, default=[1, 2, 3]):
        try:
            vals = series.dropna().astype(float).astype(int).unique()
            return sorted(set(vals))
        except Exception:
            return default

    with col4:
        st.markdown("🛏️ **Bedrooms**")
        bedroom_options = get_unique_int_values(df["bedrooms"]) if "bedrooms" in df.columns else [1, 2, 3]
        selected_bedroom = st.selectbox("Bedrooms", bedroom_options, label_visibility="collapsed")

    with col5:
        st.markdown("🛁 **Bathrooms**")
        bathroom_options = get_unique_int_values(df["bathrooms"]) if "bathrooms" in df.columns else [1, 2, 3]
        selected_bathroom = st.selectbox("Bathrooms", bathroom_options, label_visibility="collapsed")

    with col6:
        st.markdown("👨‍👩‍👧 **Guests (Adults)**")
        bed_options = get_unique_int_values(df["beds"]) if "beds" in df.columns else [1, 2, 3, 4]
        selected_beds = st.selectbox("Guests", bed_options, label_visibility="collapsed")


    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Apply Filters to Dataset --------------------
filtered_main = df.copy()

# Filter by available_date (jika ada)
if "available_date" in filtered_main.columns:
    filtered_main = filtered_main[
        (pd.to_datetime(filtered_main["available_date"], errors="coerce") <= pd.to_datetime(selected_date))
    ]

# Bedrooms filter (>=)
if "bedrooms" in filtered_main.columns:
    filtered_main = filtered_main[filtered_main["bedrooms"].fillna(0) >= selected_bedroom]

# Bathrooms filter (>=)
if "bathrooms" in filtered_main.columns:
    filtered_main = filtered_main[filtered_main["bathrooms"].fillna(0) >= selected_bathroom]

# Beds filter (>=)
if "beds" in filtered_main.columns:
    filtered_main = filtered_main[filtered_main["beds"].fillna(0) >= selected_beds]

st.markdown("---")

# -------------------- Top Stays Section --------------------
st.header(f"🏆 Top Stays for Travelers from **{user_country}**")
st.write("Find the highest-rated stays across different property types — curated for USA travelers!")

# -------------------- Filter USA Data (setelah filter card) --------------------
if "country" in filtered_main.columns:
    usa_mask = filtered_main["country"].str.contains("USA|United States|America", case=False, na=False)
    usa_df = filtered_main[usa_mask].copy() if usa_mask.sum() > 0 else filtered_main.copy()
else:
    usa_df = filtered_main.copy()


# Pastikan kolom utama ada
required_cols = ["property_type", "review_scores_rating", "number_of_reviews", "thumbnail_url", "name", "log_price", "was_price"]
for col in required_cols:
    if col not in usa_df.columns:
        usa_df[col] = None

# -------------------- Dropdown Property Type --------------------
property_types = sorted(usa_df["property_type"].dropna().unique().tolist())
selected_property = st.selectbox("🏠 Choose Property Type", property_types)

# -------------------- Filter per Property Type --------------------
filtered_df = usa_df[usa_df["property_type"] == selected_property].copy()

if filtered_df.empty:
    st.warning(f"No listings available for property type: {selected_property}")
else:
    # Urutkan berdasarkan rating tertinggi, lalu review terbanyak
    filtered_df = filtered_df.sort_values(
        ["review_scores_rating", "number_of_reviews"],
        ascending=[False, False]
    ).head(5)

    st.markdown(f"### 🌟 Top 5 **{selected_property}** in the **{user_country}**")

    # -------------------- Display Grid --------------------
    cols = st.columns(5, gap="medium")

    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[idx % 5]:
            thumb = row["thumbnail_url"] if (
                isinstance(row["thumbnail_url"], str) and row["thumbnail_url"].startswith("http")
            ) else "https://picsum.photos/300/200"

            # Gambar
            st.image(thumb, use_container_width=True)

            # Nama
            st.markdown(f"**{row['name'][:40]}**")
            bed = int(row.get("bedrooms", 0))
            bath = int(row.get("bathrooms", 0))
            guest = int(row.get("beds", 0))
            st.markdown(f"🛏️ {bed} Bedroom | 🛁 {bath} Bathroom")
            st.markdown(f"👨‍👩‍👧 {guest} Guests")

            # Rating dan jumlah review
            rating = row.get("review_scores_rating", 0)
            reviews = int(row.get("number_of_reviews", 0))
            st.markdown(f"⭐ **{rating:.1f}** ({reviews})")

            # Harga lama (dicoret)
            was_price = row.get("was_price", 0)
            st.markdown(
                f"<span style='color:gray;text-decoration:line-through;'>Was: ${was_price:.2f}</span>",
                unsafe_allow_html=True
            )

            # Harga baru (teks tebal & warna oranye)
            now_price = row.get("log_price", 0)
            st.markdown(
                f"<span style='font-weight:700;color:orange;'>Now: ${now_price:.2f}</span>",
                unsafe_allow_html=True
            )

st.markdown("---")

# -------------------- Display Grid --------------------
st.markdown(f"### ✨ Most Popular Stays **{user_country}**")

# Ambil top 5 overall (tanpa filter property_type)
popular_df = (
    usa_df.sort_values(
        ["review_scores_rating", "number_of_reviews"],
        ascending=[False, False]
    )
    .head(5)
)

cols = st.columns(5, gap="medium")

for idx, (_, row) in enumerate(popular_df.iterrows()):
    with cols[idx % 5]:
        thumb = row["thumbnail_url"] if (
            isinstance(row["thumbnail_url"], str) and row["thumbnail_url"].startswith("http")
        ) else "https://picsum.photos/300/200"

        st.image(thumb, use_container_width=True)
        st.markdown(f"**{row['name'][:40]}**")
        bed = int(row.get("bedrooms", 0))
        bath = int(row.get("bathrooms", 0))
        guest = int(row.get("beds", 0))
        st.markdown(f"🛏️ {bed} Bedroom | 🛁 {bath} Bathroom")
        st.markdown(f"👨‍👩‍👧 {guest} Guests")

        rating = row.get("review_scores_rating", 0)
        reviews = int(row.get("number_of_reviews", 0))
        st.markdown(f"⭐ **{rating:.1f}** ({reviews})")

        was_price = row.get("was_price", 0)
        st.markdown(
            f"<span style='color:gray;text-decoration:line-through;'>Was: ${was_price:.2f}</span>",
            unsafe_allow_html=True
        )

        now_price = row.get("log_price", 0)
        st.markdown(
            f"<span style='font-weight:700;color:orange;'>Now: ${now_price:.2f}</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
# -------------------- Top Activities --------------------
st.header(f"🎯 Top Activities for **{user_country}** Traveler’s Picks")
st.write("Explore our best-in-class destinations, loved and recommended by our guests across the United States!")

# -------------------- Filter Country --------------------
if "country" in df.columns:
    usa_mask = df["country"].str.contains("USA|United States|America", case=False, na=False)
    usa_df = df[usa_mask].copy() if usa_mask.sum() > 0 else df.copy()
else:
    usa_df = df.copy()

# Pastikan kolom utama tersedia
required_cols = ["specification", "review_scores_rating", "number_of_reviews", "thumbnail_url", "name"]
for col in required_cols:
    if col not in usa_df.columns:
        usa_df[col] = None

# -------------------- Activity Dropdown Filter --------------------
activity_options = [
    "Near Airport", "Near Art Alley", "Near Art Gallery", "Near Art Lane", "Near Art Market", "Near Art Street",
    "Near Artisan Market", "Near Beach", "Near Beach Walk", "Near Beachfront", "Near Botanical Garden",
    "Near Boutique Street", "Near Business District", "Near Business Hub", "Near Camping Spot", "Near Central Park",
    "Near City Center", "Near City Market", "Near City Museum", "Near Cliff Trail", "Near Cliff View",
    "Near Cliff Viewpoint", "Near Coastal Boardwalk", "Near Coffee Quarter", "Near Concert Arena",
    "Near Convention Hall", "Near Creative District", "Near Creative Hub", "Near Cultural Market",
    "Near Cultural Village", "Near Downtown", "Near Downtown Street", "Near Food Street", "Near Forest Edge",
    "Near Forest Reserve", "Near Forest Retreat", "Near Forest Trail", "Near Golf Course", "Near Golf Park",
    "Near Harbor View", "Near Harbor Walk", "Near Harborfront", "Near Heritage District", "Near Heritage Town",
    "Near Hiking Trail", "Near Hilltop Café", "Near Historical Museum", "Near Lake Garden", "Near Lake Trail",
    "Near Lakefront", "Near Lakeside Pavilion", "Near Lookout Point", "Near Marina Bay", "Near Marina Pier",
    "Near Market", "Near Mountain Peak", "Near Mountain Trail", "Near Mountain Valley", "Near Mountain View",
    "Near National Park", "Near Nature Reserve", "Near Night Bazaar", "Near Night Street", "Near Nightlife Area",
    "Near Ocean Breeze Point", "Near Ocean Point", "Near Ocean Viewpoint", "Near Oceanfront", "Near Old Town",
    "Near Open Air Café", "Near Park District", "Near Pedestrian Bridge", "Near Picnic Ground", "Near Rice Terrace",
    "Near River View", "Near Riverbank", "Near Riverbank Trail", "Near Riverbank Walk", "Near Riverside Café",
    "Near Riverside Garden", "Near Riverside Lodge", "Near Riverside Walk", "Near Riverwalk", "Near Rooftop Bar",
    "Near Scenic Park", "Near Seafood Market", "Near Shopping Avenue", "Near Shopping District", "Near Shopping Mall",
    "Near Shopping Promenade", "Near Shopping Street", "Near Surf Spot", "Near Sunset Bar", "Near Sunset Point",
    "Near Sunset View", "Near Stadium", "Near Temple", "Near Temple Courtyard", "Near Train Station", "Near Urban Park",
    "Near Valley View", "Near Village Café", "Near Village View", "Near Village Walk", "Near Waterfall View"
]

# Dropdown multiselect
selected_activities = st.multiselect(
    "🏖️ Choose Nearby Attractions",
    options=sorted(activity_options),
    placeholder="Select one or more nearby areas..."
)

# -------------------- Filter berdasarkan dropdown --------------------
if selected_activities:
    spec_filled = usa_df["specification"].fillna("").str.lower()

    if len(selected_activities) == 1:
        # 1 pilihan → sistem seperti LIKE '%Near Art Gallery%'
        keyword = selected_activities[0].lower()
        filtered = usa_df[spec_filled.str.contains(keyword)]
    else:
        # Lebih dari 1 pilihan → semua keyword harus muncul (AND)
        filtered = usa_df[
            spec_filled.apply(
                lambda x: all(k.lower() in x for k in selected_activities)
            )
        ].copy()
else:
    filtered = usa_df.copy()

# -------------------- Sort & Display --------------------
if filtered.empty:
    st.warning("No listings found for the selected activity area(s).")
else:
    filtered = filtered.sort_values(
        ["review_scores_rating", "number_of_reviews"],
        ascending=[False, False]
    ).head(5)

    title_text = ", ".join(selected_activities) if selected_activities else "Top Activities Overall"
    st.markdown(f"### 🏖️ Traveler’s Picks: **{title_text}**")

    cols = st.columns(5, gap="medium")
    for idx, (_, row) in enumerate(filtered.iterrows()):
        with cols[idx % 5]:
            thumb = row["thumbnail_url"] if (
                isinstance(row["thumbnail_url"], str) and row["thumbnail_url"].startswith("http")
            ) else "https://picsum.photos/300/200"

            st.image(thumb, use_container_width=True)
            st.markdown(f"**{row['name'][:40]}**")
            bed = int(row.get("bedrooms", 0))
            bath = int(row.get("bathrooms", 0))
            guest = int(row.get("beds", 0))
            st.markdown(f"🛏️ {bed} Bedroom | 🛁 {bath} Bathroom")
            st.markdown(f"👨‍👩‍👧 {guest} Guests")

            rating = row.get("review_scores_rating", 0)
            reviews = int(row.get("number_of_reviews", 0))
            st.markdown(f"⭐ **{rating:.1f}** ({reviews})")

            spec_text = row.get("specification", "")
            st.markdown(f"<span style='color:gray;font-size:13px;'>{spec_text}</span>", unsafe_allow_html=True)

st.markdown("---")

# -------------------- Special Deals --------------------
st.header("💎 Special Deals for You")
st.write("Exclusive discounts and package deals — tailored to frequent travelers.")

# Ambil property type dari filter sebelumnya
selected_type = st.session_state.get("selected_property_type", None)

# Pastikan kolom penting tersedia
required_cols = [
    "property_type", "latitude", "longitude", "name", "specification",
    "log_price", "was_price", "thumbnail_url"
]
for col in required_cols:
    if col not in df.columns:
        df[col] = None

# Filter sesuai property_type jika ada
if selected_type:
    subset = df[df["property_type"].str.lower() == selected_type.lower()].copy()
else:
    subset = df.copy()

# Cari pasangan properti yang berdekatan
if not subset.empty and len(subset) > 1:
    subset = subset.sort_values(by=["latitude", "longitude"], ascending=True).reset_index(drop=True)
    bundles = [(subset.iloc[i], subset.iloc[i + 1]) for i in range(0, len(subset) - 1, 2)]
else:
    bundles = []

# Kalau data kurang dari 3 bundle, ambil random fallback
if len(bundles) < 3:
    random_df = df.sample(min(6, len(df)), random_state=np.random.randint(0, 9999)).reset_index(drop=True)
    bundles = [(random_df.iloc[i], random_df.iloc[i + 1]) for i in range(0, len(random_df) - 1, 2)]

# Pilih 3 bundle random agar setiap refresh berbeda
import random
if bundles:
    bundles = random.sample(bundles, k=min(3, len(bundles)))

# -------------------- Display Bundles --------------------
cols = st.columns(3)
for i, (prop1, prop2) in enumerate(bundles):
    with cols[i % 3]:
        img_url = (
            prop1["thumbnail_url"]
            if isinstance(prop1["thumbnail_url"], str) and prop1["thumbnail_url"].startswith("http")
            else "https://picsum.photos/400/250"
        )
        st.image(img_url, use_container_width=True)

        st.markdown(f"**{prop1['name']}**")
        st.markdown(f"<span style='color:gray;font-size:13px;'>{prop1['specification']}</span>", unsafe_allow_html=True)

        st.markdown(f"**{prop2['name']}**")
        st.markdown(f"<span style='color:gray;font-size:13px;'>{prop2['specification']}</span>", unsafe_allow_html=True)

        def safe_float(x):
            try:
                return float(x)
            except (TypeError, ValueError):
                return 0.0

        was_1, was_2 = safe_float(prop1["was_price"]), safe_float(prop2["was_price"])
        total_was = was_1 + was_2

        price_1, price_2 = safe_float(prop1["log_price"]), safe_float(prop2["log_price"])
        total_price = price_1 + price_2


        st.markdown(
            f"<span style='text-decoration:line-through;color:gray;'>"
            f"$ {was_1:,.0f} + $ {was_2:,.0f} = $ {total_was:,.0f}"
            f"</span>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<span style='font-weight:800;color:orange;'>"
            f"Now: $ {total_price:,.0f}"
            f"</span>",
            unsafe_allow_html=True
        )

        discount_pct = 0
        if total_was > 0:
            discount_pct = (1 - total_price / total_was) * 100
        st.markdown(
            f"<span style='color:#16a34a;font-weight:700;'>💰 Save {discount_pct:.1f}%</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
# -------------------- Travel Tips Banner Image --------------------
image4_path = "images/image4.png"
if os.path.exists(image4_path):
    b64_image = img_file_to_base64(image4_path)
    HERO_HEIGHT_PX = 600  # sama seperti hero slider
    st.markdown(
        f"""
        <div style="width:100%;height:{HERO_HEIGHT_PX}px;overflow:hidden;">
            <img src="data:image/png;base64,{b64_image}" 
                 style="width:100%;height:100%;object-fit:cover;border-radius:12px;" />
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ image4.png not found in 'images/' folder")

# -------------------- Travel Tips --------------------
st.header(f"Travel Tips from Indonesia to {user_country}")
st.write("Practical info to help you prepare: flight duration, transport, SIM card, visa, and cultural tips.")

st.subheader("Quick Practical Tips")
st.markdown("- **Flight duration:** Varies by route; typically 7–20 hours depending on connections.")
st.markdown("- **Transport:** Use local rideshares or public transit. Check airport transfer options ahead of time.")
st.markdown("- **SIM card / eSIM:** Buy at the airport or pre-order an international eSIM for convenience.")
st.markdown("- **Visa:** Check official consulate for the latest requirements.")
st.markdown("- **Cultural tips:** Respect local customs and tipping practices. Learn a few local phrases — hosts appreciate it!")

# -------------------- Footer --------------------
st.markdown(
    """
    <style>
    .footer {
        position: relative;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 25px 0;
        font-size: 14px;
        color: #555;
        background: rgba(255,255,255,0.5);
        border-top: 1px solid rgba(0,0,0,0.1);
        margin-top: 80px;
    }
    </style>
    <div class="footer">
        © Okaviantama Karunia Haris — All rights reserved
    </div>
    """,
    unsafe_allow_html=True,
)
