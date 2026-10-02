import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import shutil
import random
import plotly.express as px
from datetime import datetime
import io
import re

# Page Configuration
st.set_page_config(
    page_title="Google Maps Scraper Pro",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Glassmorphic iPhone-style UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #02092b 0%, #764ba2 100%) !important;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem !important;
        max-width: 100% !important;
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    .stButton>button {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
    }
    
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .stMarkdown {
        color: rgba(255, 255, 255, 0.9);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .business-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .business-card:hover {
        background: rgba(255, 255, 255, 0.18);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    .business-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .business-rating {
        display: inline-block;
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        color: #333;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .business-info {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem;
        background: rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .success-badge {
        background: rgba(74, 222, 128, 0.3);
        border: 2px solid #4ade80;
    }
    
    .warning-badge {
        background: rgba(251, 146, 60, 0.3);
        border: 2px solid #fb923c;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = []
if 'scraping_active' not in st.session_state:
    st.session_state.scraping_active = False
if 'live_metrics' not in st.session_state:
    st.session_state.live_metrics = {'listings': 0, 'unique': 0, 'progress': 0}

# Helper function to format US phone numbers
def format_us_phone(phone_text):
    """Extract and format US phone numbers"""
    if not phone_text or phone_text == "N/A":
        return "N/A"
    
    cleaned = re.sub(r'[^\d+]', '', phone_text)
    
    if cleaned.startswith('+1'):
        digits = cleaned[2:]
    elif cleaned.startswith('1') and len(cleaned) == 11:
        digits = cleaned[1:]
    elif len(cleaned) == 10:
        digits = cleaned
    else:
        return phone_text
    
    if len(digits) == 10:
        return f"+1 {digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
    
    return phone_text

# Enhanced scraping function with visible browser option
def scrape_google_maps(url, max_duration, max_results, region, status_placeholder, progress_bar, browser_mode="Headless (No Browser)"):
    """
    Enhanced Google Maps scraper with visible browser and aggressive auto-scrolling
    """
    options = Options()
    
    # Configure browser based on mode
    if browser_mode == "Headless (No Browser)":
        options.add_argument("--headless")
    else:
        # Visible browser settings
        options.add_argument("--start-maximized")
        if browser_mode == "Side Panel View":
            options.add_argument("--window-size=800,1000")
            options.add_argument("--window-position=1100,0")
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    scraped_businesses = []
    seen_names = set()
    
    try:
            status_placeholder.markdown(
                "🚀 **Initializing Chrome driver...**"
            )

            chromium_path = (
                shutil.which("chromium")
                or shutil.which("chromium-browser")
                or shutil.which("google-chrome")
            )
            chromedriver_path = shutil.which("chromedriver")

            if chromium_path and chromedriver_path:
                options.binary_location = chromium_path
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")

                driver = webdriver.Chrome(
                    service=Service(chromedriver_path),
                    options=options
                )
            else:
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )

            status_placeholder.markdown(
                "🌐 **Loading Google Maps URL...**"
            )
            driver.get(url)
        
        # Longer wait for visible browser
                    wait_time = 10 if browser_mode != "Headless (No Browser)" else 8
        
        status_placeholder.markdown("🔍 **Finding scrollable container...**")
        
        # Find the scrollable results container with multiple strategies
        scrollable_div = None
        selectors = [
            '//div[@role="feed"]',
            '//div[contains(@class, "m6QErb")]',
            '//div[@role="main"]',
            '//div[contains(@aria-label, "Results")]',
            '//div[contains(@class, "feed")]'
        ]
        
        for selector in selectors:
            try:
                scrollable_div = driver.find_element(By.XPATH, selector)
                status_placeholder.markdown(f"✅ **Found scrollable container!**")
                break
            except:
                continue
        
        if not scrollable_div:
            scrollable_div = driver.find_element(By.TAG_NAME, 'body')
        
        start_time = time.time()
        last_height = 0
        no_change_count = 0
        scroll_attempt = 0
        consecutive_no_new_listings = 0
        
        status_placeholder.markdown("🔄 **Starting SUPER aggressive auto-scroll...**")
        
        while time.time() - start_time < max_duration and len(scraped_businesses) < max_results:
            scroll_attempt += 1
            previous_count = len(scraped_businesses)
            
            try:
                # Get current scroll height
                current_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                
                # SUPER AGGRESSIVE MULTI-SCROLL STRATEGY
                # Phase 1: Rapid small scrolls (simulates user scrolling)
                for i in range(8):
                    scroll_amount = random.randint(300, 500)
                    driver.execute_script(f"arguments[0].scrollBy(0, {scroll_amount});", scrollable_div)
                    time.sleep(0.15)
                
                # Phase 2: Medium scroll
                driver.execute_script("arguments[0].scrollBy(0, 1000);", scrollable_div)
                time.sleep(0.5)
                
                # Phase 3: Scroll to absolute bottom
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(random.uniform(2.0, 3.0))
                
                # Check for "You've reached the end" message
                try:
                    end_message = driver.find_element(By.XPATH, '//*[contains(text(), "reached the end") or contains(text(), "no more results")]')
                    if end_message:
                        status_placeholder.markdown("✅ **Reached end of all results**")
                        break
                except:
                    pass
                
                # Check for new content
                new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                
                if new_height == last_height:
                    no_change_count += 1
                    status_placeholder.markdown(f"⚠️ **No height change detected (attempt {no_change_count}/5)**")
                    
                    # Advanced stuck detection - try multiple recovery techniques
                    if no_change_count >= 2:
                        status_placeholder.markdown("🔄 **Executing scroll recovery techniques...**")
                        
                        # Technique 1: Scroll to top then bottom
                        driver.execute_script("arguments[0].scrollTop = 0", scrollable_div)
                        time.sleep(1.0)
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                        time.sleep(2.0)
                        
                        # Technique 2: Click on a listing to trigger loading
                        try:
                            listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/maps/place/")]')
                            if listings and len(listings) > 5:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", listings[-3])
                                time.sleep(1.5)
                        except:
                            pass
                        
                        # Technique 3: Aggressive rapid scrolling
                        for _ in range(15):
                            driver.execute_script("arguments[0].scrollBy(0, 400);", scrollable_div)
                            time.sleep(0.1)
                        
                        time.sleep(2.5)
                        no_change_count = 0
                    
                    # If truly stuck after recovery attempts
                    if no_change_count >= 5:
                        status_placeholder.markdown("⏹️ **Maximum scroll attempts reached**")
                        break
                else:
                    no_change_count = 0
                    last_height = new_height
                    status_placeholder.markdown(f"✅ **New content loaded! Scroll height: {new_height}px**")
                
                # Extract all visible listings with multiple selectors
                listing_selectors = [
                    '//div[contains(@class, "Nv2PK")]',
                    '//div[contains(@jsaction, "mouseover")]',
                    '//div[contains(@class, "THOPZb")]',
                    '//a[contains(@class, "hfpxzc")]/..',
                    '//div[@role="article"]'
                ]
                
                all_listings = []
                for selector in listing_selectors:
                    try:
                        found = driver.find_elements(By.XPATH, selector)
                        all_listings.extend(found)
                    except:
                        continue
                
                # Remove duplicates
                listings = list(set(all_listings))
                
                status_placeholder.markdown(f"📋 **Found {len(listings)} visible listings on page | Extracted: {len(scraped_businesses)}/{max_results}**")
                
                for listing in listings:
                    if len(scraped_businesses) >= max_results:
                        break
                    
                    try:
                        # Extract business name with multiple strategies
                        name = "N/A"
                        name_selectors = [
                            './/div[@class="qBF1Pd fontHeadlineSmall"]',
                            './/div[contains(@class, "fontHeadlineSmall")]',
                            './/div[@class="qBF1Pd"]',
                            './/a[contains(@class, "hfpxzc")]',
                            './/div[contains(@class, "fontBodyMedium")]'
                        ]
                        
                        for selector in name_selectors:
                            try:
                                name_elem = listing.find_element(By.XPATH, selector)
                                name = name_elem.text.strip()
                                if name and len(name) > 2:
                                    break
                            except:
                                continue
                        
                        if not name or name == "N/A" or name in seen_names:
                            continue
                        
                        seen_names.add(name)
                        
                        # Extract rating with improved selectors
                        rating = "N/A"
                        try:
                            rating_elem = listing.find_element(By.XPATH, './/span[@role="img"]')
                            rating_text = rating_elem.get_attribute('aria-label')
                            if rating_text:
                                rating_match = re.search(r'(\d+\.?\d*)\s*star', rating_text)
                                if rating_match:
                                    rating = rating_match.group(1)
                        except:
                            try:
                                rating = listing.find_element(By.CLASS_NAME, 'MW4etd').text.strip()
                            except:
                                pass
                        
                        # Extract reviews count with improved regex
                        reviews = "N/A"
                        try:
                            reviews_selectors = [
                                './/span[contains(text(), "reviews") or contains(text(), "review")]',
                                './/span[contains(@aria-label, "reviews")]'
                            ]
                            for selector in reviews_selectors:
                                try:
                                    reviews_elem = listing.find_element(By.XPATH, selector)
                                    reviews_text = reviews_elem.text
                                    reviews_match = re.search(r'\(?([\d,]+)\)?', reviews_text)
                                    if reviews_match:
                                        reviews = reviews_match.group(1).replace(',', '')
                                        break
                                except:
                                    continue
                        except:
                            pass
                        
                        # Extract phone with improved detection
                        phone = "N/A"
                        phone_selectors = [
                            './/span[contains(text(), "+")]',
                            './/a[contains(@href, "tel:")]',
                            './/span[contains(@aria-label, "Phone")]',
                            './/button[contains(@aria-label, "Phone")]'
                        ]
                        
                        for selector in phone_selectors:
                            try:
                                phone_elem = listing.find_element(By.XPATH, selector)
                                href = phone_elem.get_attribute('href')
                                if href and 'tel:' in href:
                                    phone = href.replace('tel:', '').strip()
                                else:
                                    phone = phone_elem.text.strip()
                                
                                if phone and phone != "N/A" and len(phone) > 5:
                                    if region in ["United States", "Canada"]:
                                        phone = format_us_phone(phone)
                                    break
                            except:
                                continue
                        
                        # Extract address with improved selectors
                        address = "N/A"
                        address_selectors = [
                            './/div[@class="W4Efsd"]',
                            './/div[contains(@class, "W4Efsd")]',
                            './/span[contains(@class, "LrzXr")]',
                            './/div[contains(@class, "rogA2c")]'
                        ]
                        
                        for selector in address_selectors:
                            try:
                                address_elem = listing.find_element(By.XPATH, selector)
                                address_text = address_elem.text
                                address_parts = address_text.split('·')
                                if len(address_parts) > 0:
                                    address = address_parts[-1].strip()
                                    if address and len(address) > 5:
                                        break
                            except:
                                continue
                        
                        # Extract website/URL
                        place_url = "N/A"
                        try:
                            link_elem = listing.find_element(By.XPATH, './/a[contains(@href, "/maps/place/")]')
                            place_url = link_elem.get_attribute('href')
                        except:
                            pass
                        
                        scraped_businesses.append({
                            "Name": name,
                            "Rating": rating,
                            "Reviews": reviews,
                            "Phone": phone,
                            "Address": address,
                            "Place_URL": place_url,
                            "Search_URL": url,
                            "Region": region,
                            "Scraped_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Update live metrics
                        st.session_state.live_metrics['unique'] = len(seen_names)
                        st.session_state.live_metrics['listings'] = len(scraped_businesses)
                        
                    except Exception as e:
                        continue
                
                # Check if we got new listings
                new_listings = len(scraped_businesses) - previous_count
                if new_listings == 0:
                    consecutive_no_new_listings += 1
                    status_placeholder.markdown(f"⚠️ **No new listings found (attempt {consecutive_no_new_listings}/4)**")
                    
                    if consecutive_no_new_listings >= 4:
                        status_placeholder.markdown("🛑 **No new listings after multiple attempts - likely reached end**")
                        break
                else:
                    consecutive_no_new_listings = 0
                    status_placeholder.markdown(f"✨ **Found {new_listings} new listings!**")
                
                # Update progress
                progress = min((len(scraped_businesses) / max_results) * 100, 100)
                progress_bar.progress(int(progress))
                
                # Update status every 5 results
                if len(scraped_businesses) % 5 == 0 and len(scraped_businesses) > 0:
                    elapsed_time = time.time() - start_time
                    speed = len(scraped_businesses) / elapsed_time if elapsed_time > 0 else 0
                    status_placeholder.markdown(f"""
                    <div class='status-badge success-badge'>
                        ✅ Scraped {len(scraped_businesses)} businesses | Scroll #{scroll_attempt} | Speed: {speed:.1f}/sec
                    </div>
                    """, unsafe_allow_html=True)
                
                # Strategic pause every 20 scrolls
                if scroll_attempt % 20 == 0:
                    time.sleep(random.uniform(2.0, 3.5))
                    
            except Exception as e:
                status_placeholder.markdown(f"⚠️ **Scroll error: {str(e)}**")
                continue
        
        elapsed_total = int(time.time() - start_time)
        status_placeholder.markdown(f"""
        <div class='status-badge success-badge'>
            ✅ Scraping completed! Collected {len(scraped_businesses)} unique businesses in {elapsed_total}s
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        status_placeholder.markdown(f"""
        <div class='status-badge warning-badge'>
            ❌ Error: {str(e)}
        </div>
        """, unsafe_allow_html=True)
    
    finally:
        if driver and browser_mode == "Headless (No Browser)":
            driver.quit()
        elif driver:
            # Keep browser open for 5 seconds in visible mode
            status_placeholder.markdown("⏳ **Keeping browser open for 5 seconds...**")
            time.sleep(5)
            driver.quit()
    
    return scraped_businesses

# Sidebar Configuration
with st.sidebar:
    st.title("🗺️ Scraper Configuration")
    
    region = st.selectbox(
        "📍 Target Region",
        ["United States", "India", "Canada", "UK", "Australia"]
    )
    
    scraping_mode = st.selectbox(
        "Scraping Mode",
        ["Custom Search", "Multiple URLs", "Predefined Locations"]
    )
    
    st.markdown("---")
    
    if scraping_mode == "Custom Search":
        st.subheader("Custom Search Options")
        search_query = st.text_input("Search Query", "restaurants")
        
        if region == "United States":
            location = st.text_input("Location", "New York, NY")
        elif region == "India":
            location = st.text_input("Location", "Mumbai")
        elif region == "Canada":
            location = st.text_input("Location", "Toronto, ON")
        elif region == "UK":
            location = st.text_input("Location", "London")
        else:
            location = st.text_input("Location", "Sydney")
            
    elif scraping_mode == "Multiple URLs":
        st.subheader("URL Input")
        url_input = st.text_area(
            "Enter URLs (one per line)",
            height=200,
            placeholder="https://www.google.com/maps/search/..."
        )
        
    else:
        st.subheader(f"{region} Locations")
        
        if region == "United States":
            locations = [
                "Manhattan, NY", "Brooklyn, NY", "Queens, NY", "Los Angeles, CA",
                "San Francisco, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ"
            ]
        elif region == "India":
            locations = [
                "Churchgate", "Marine Lines", "Bandra", "Andheri", "Dadar",
                "Lower Parel", "Powai", "Thane"
            ]
        elif region == "Canada":
            locations = ["Downtown Toronto", "North York", "Vancouver", "Montreal"]
        elif region == "UK":
            locations = ["Westminster", "Camden", "Shoreditch", "Manchester"]
        else:
            locations = ["Sydney CBD", "Melbourne CBD", "Brisbane City"]
            
        selected_locations = st.multiselect(
            "Select Locations",
            locations,
            default=locations[:3]
        )
        company_type = st.text_input("Business Type", "restaurants")
    
    st.markdown("---")
    
    st.subheader("⚙️ Scraping Settings")
    max_results = st.number_input("Max Results per URL", 50, 2000, 500, 50)
    max_duration = st.slider("Duration per URL (seconds)", 30, 300, 180, 10)
    
    st.markdown("---")
    
    st.subheader("🖥️ Browser Display Mode")
    browser_mode = st.radio(
        "Choose Display Option:",
        ["Headless (No Browser)", "Visible Browser (External Window)", "Side Panel View"],
        help="Choose how you want to see the scraping process"
    )
    
    if browser_mode == "Visible Browser (External Window)":
        st.success("✅ Browser will open in a separate window")
        st.info("💡 You can watch the live scraping process!")
    elif browser_mode == "Side Panel View":
        st.warning("⚠️ Limited view - External window recommended for debugging")
    else:
        st.info("⚡ Fastest mode - No browser window")
    
    st.markdown("---")
    
    # NEW: Real-time Map Viewer Option
    st.subheader("🌐 Live Map Viewer")
    show_live_map = st.checkbox("Show Live Google Maps Preview", value=False)
    
    if show_live_map:
        st.info("📍 Map will update below when you start scraping")
        
        # Generate preview URL
        if scraping_mode == "Custom Search":
            preview_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}+{location.replace(' ', '+')}"
        elif scraping_mode == "Multiple URLs" and url_input and url_input.strip():
            preview_url = url_input.split('\n')[0].strip()
        else:
            preview_url = f"https://www.google.com/maps/search/restaurants+{region.replace(' ', '+')}"
        
        # Open in new tab button
        st.link_button("🔗 Open in New Browser Tab", preview_url, use_container_width=True)
        
        # Embedded iframe
        st.markdown('<div style="border: 2px solid rgba(255,255,255,0.3); border-radius: 10px; overflow: hidden; margin-top: 10px;">', unsafe_allow_html=True)
        st.components.v1.iframe(preview_url, height=400, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.caption("💡 Tip: Use the 'Open in New Browser Tab' button for better manual scrolling control")
    
    url_count = 1
    if scraping_mode == "Multiple URLs" and url_input:
        url_count = len([u for u in url_input.split('\n') if u.strip()])
    elif scraping_mode == "Predefined Locations":
        url_count = len(selected_locations) if selected_locations else 0
    
    st.info(f"""
    **Current Settings:**
    - Max Results: {max_results}
    - Duration: {max_duration}s per URL
    - Browser Mode: {browser_mode}
    - URLs to scrape: {url_count}
    - Estimated time: {max_duration * url_count}s
    """)
    
    st.markdown("---")
    
    st.subheader("💾 Export Options")
    export_format = st.radio("Export Format", ["Excel (.xlsx)", "CSV (.csv)", "Both"])

# Main Content
st.title("🗺️ Google Maps Business Scraper Pro")
st.markdown(f"### Advanced data extraction with aggressive auto-scroll - {region}")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Scraper", "📊 Analytics", "🗺️ Map View", "📥 Export"])

with tab1:
    # Add Live Map Viewer at the top
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_map1, col_map2 = st.columns([3, 1])
    
    with col_map1:
        st.subheader("🌐 Live Google Maps Preview")
    
    with col_map2:
        show_live_map = st.checkbox("Enable Live Preview", value=False)
    
    if show_live_map:
        # Generate preview URL
        if scraping_mode == "Custom Search":
            preview_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}+{location.replace(' ', '+')}"
        elif scraping_mode == "Multiple URLs" and url_input and url_input.strip():
            preview_url = url_input.split('\n')[0].strip()
        else:
            preview_url = f"https://www.google.com/maps/search/restaurants+{region.replace(' ', '+')}"
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            st.link_button("🔗 Open in New Tab", preview_url, use_container_width=True)
        with col_btn2:
            if st.button("🔄 Refresh Map", use_container_width=True):
                st.rerun()
        
        st.components.v1.iframe(preview_url, height=500, scrolling=True)
        st.info("💡 Tip: Click 'Open in New Tab' for full manual scrolling control while scraper runs")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Original content continues
    if browser_mode == "Side Panel View":
        col1, col2 = st.columns([3, 2])
    else:
        col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Scraping Control Panel")
        
        start_button = st.button("🚀 Start Scraping", use_container_width=True, type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if start_button:
            st.session_state.scraping_active = True
            st.session_state.scraped_data = []
            st.session_state.live_metrics = {'listings': 0, 'unique': 0, 'progress': 0}
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            progress_bar = st.progress(0)
            status_placeholder = st.empty()
            
            # Generate URLs
            urls = []
            if scraping_mode == "Custom Search":
                urls = [f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}+{location.replace(' ', '+')}"]
            elif scraping_mode == "Multiple URLs":
                urls = [url.strip() for url in url_input.split('\n') if url.strip()]
            else:
                urls = [
                    f"https://www.google.com/maps/search/{company_type.replace(' ', '+')}+{loc.replace(' ', '+')}"
                    for loc in selected_locations
                ]
            
            all_data = []
            
            for idx, url in enumerate(urls):
                st.markdown(f"### 🔍 Scraping URL {idx+1}/{len(urls)}")
                st.code(url, language=None)
                
                scraped = scrape_google_maps(
                    url=url,
                    max_duration=max_duration,
                    max_results=max_results,
                    region=region,
                    status_placeholder=status_placeholder,
                    progress_bar=progress_bar,
                    browser_mode=browser_mode
                )
                
                all_data.extend(scraped)
                st.success(f"✅ Collected {len(scraped)} businesses from this URL")
                
                if idx < len(urls) - 1:
                    st.info("⏳ Waiting 3 seconds before next URL...")
                    time.sleep(3)
            
            st.session_state.scraped_data = all_data
            st.session_state.scraping_active = False
            
            st.balloons()
            st.success(f"🎉 **Scraping completed!** Total: **{len(all_data)}** unique businesses")
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Live Metrics")
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.live_metrics['listings']}</div>
            <div class="metric-label">Total Listings</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.live_metrics['unique']}</div>
            <div class="metric-label">Unique Businesses</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display latest scraped businesses
    if st.session_state.scraped_data:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Latest Scraped Businesses")
        
        for business in st.session_state.scraped_data[-10:]:
            rating_html = f'<span class="business-rating">⭐ {business["Rating"]} ({business["Reviews"]} reviews)</span>' if business["Rating"] != "N/A" else ""
            
            st.markdown(f"""
            <div class="business-card">
                <div class="business-name">{business['Name']}</div>
                {rating_html}
                <div class="business-info">
                    📞 <strong>Phone:</strong> {business['Phone']}<br>
                    📍 <strong>Address:</strong> {business['Address']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if st.session_state.scraped_data:
        df = pd.DataFrame(st.session_state.scraped_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("With Phone", len(df[df['Phone'] != 'N/A']))
        with col3:
            st.metric("With Rating", len(df[df['Rating'] != 'N/A']))
        with col4:
            avg_rating = df[df['Rating'] != 'N/A']['Rating'].astype(float).mean() if len(df[df['Rating'] != 'N/A']) > 0 else 0
            st.metric("Avg Rating", f"{avg_rating:.2f}⭐")
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Complete Data Table")
        st.dataframe(df, use_container_width=True, height=500)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No data available. Start scraping to see analytics.")

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Live Map View")
    
    if scraping_mode == "Custom Search":
        map_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}+{location.replace(' ', '+')}"
    elif scraping_mode == "Multiple URLs" and url_input.strip():
        map_url = url_input.split('\n')[0].strip()
    else:
        map_url = f"https://www.google.com/maps/search/restaurants+{region.replace(' ', '+')}"
    
    st.components.v1.iframe(map_url, height=600, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    if st.session_state.scraped_data:
        df = pd.DataFrame(st.session_state.scraped_data)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💾 Export Your Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Excel Export
            if export_format in ["Excel (.xlsx)", "Both"]:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Scraped Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name=f"gmaps_{region.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col2:
            # CSV Export
            if export_format in ["CSV (.csv)", "Both"]:
                csv = df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"gmaps_{region.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data Summary
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Export Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='text-align: center; color: white;'>
                <h3 style='color: #ffd700;'>{len(df)}</h3>
                <p>Total Records</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with_phone = len(df[df['Phone'] != 'N/A'])
            st.markdown(f"""
            <div style='text-align: center; color: white;'>
                <h3 style='color: #4ade80;'>{with_phone}</h3>
                <p>With Phone Numbers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            with_rating = len(df[df['Rating'] != 'N/A'])
            st.markdown(f"""
            <div style='text-align: center; color: white;'>
                <h3 style='color: #fb923c;'>{with_rating}</h3>
                <p>With Ratings</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample data preview
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👁️ Data Preview (First 5 Results)")
        
        for idx, business in df.head(5).iterrows():
            rating_display = f"⭐ {business['Rating']}" if business['Rating'] != 'N/A' else "No rating"
            reviews_display = f"({business['Reviews']} reviews)" if business['Reviews'] != 'N/A' else ""
            
            st.markdown(f"""
            <div class="business-card">
                <div class="business-name">{business['Name']}</div>
                <span class="business-rating">{rating_display} {reviews_display}</span>
                <div class="business-info">
                    📞 <strong>Phone:</strong> {business['Phone']}<br>
                    📍 <strong>Address:</strong> {business['Address']}<br>
                    🌍 <strong>Region:</strong> {business['Region']}<br>
                    🔗 <strong>Place URL:</strong> <a href="{business['Place_URL']}" target="_blank" style="color: #4ade80;">View on Maps</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No data to export. Start scraping first!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255, 255, 255, 0.7);'>
    <p>🗺️ Google Maps Scraper Pro | Built with Streamlit & Selenium</p>
    <p style='font-size: 0.85rem;'>✨ Features SUPER aggressive auto-scroll for maximum data extraction</p>
    <p style='font-size: 0.85rem;'>Supports US (+1), India (+91), Canada (+1), UK (+44), Australia (+61)</p>
    <p style='font-size: 0.85rem;'>💡 Use "Visible Browser" mode to watch live scraping!</p>
</div>
""", unsafe_allow_html=True)
