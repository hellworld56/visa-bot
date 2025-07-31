# from playwright.sync_api import sync_playwright
# import time
# import os
# import sys


# def wait_for_available_slot_and_click(page):
#     print("Waiting for standard appointment slot...")

#     while True:
#         try:
#             slot_buttons = page.locator("button[data-testid='btn-available-slot']:visible")
#             count = slot_buttons.count()

#             if count > 0:
#                 for i in range(count):
#                     button = slot_buttons.nth(i)
#                     label_span = button.locator("span.sr-only")

#                     if label_span.count() > 0:
#                         label_text = label_span.inner_text().strip().lower()

#                         if "standard appointment" in label_text:
#                             button.wait_for(state="visible", timeout=3000)
#                             time_text = button.inner_text().strip()
#                             button.click()
#                             print(f"Clicked standard appointment slot: {time_text}")
#                             return

#                 print("No standard appointment slots available right now.")
#             else:
#                 print("No available slot buttons found.")
#         except Exception as e:
#             print(f"Error checking for standard slot: {e}")

#         print("Retrying in 15s...")
#         time.sleep(15)
#         page.reload()
#         page.wait_for_load_state("networkidle")


# def login_and_book():
#     email = os.getenv("BOT_EMAIL")
#     password = os.getenv("BOT_PASSWORD")
#     country = os.getenv("BOT_COUNTRY")

#     if not email or not password or not country:
#         print("❌ Missing EMAIL, PASSWORD or COUNTRY environment variable.")
#         sys.exit(1)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#         headless=True,
#         proxy={
#             "server": "http://eu.decodo.com:10000",
#             "username": "spkm1bz91s",
#             "password": "ybkhaU9Bn+3g1ns4KP"
#         }
#         )

#         context = browser.new_context(
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                 "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
#             ),
#             viewport={"width": 1280, "height": 720},
#             java_script_enabled=True,
#             ignore_https_errors=True,
#         )

#         context.set_extra_http_headers({
#             "Accept-Language": "en-US,en;q=0.9",
#             "DNT": "1",
#             "Upgrade-Insecure-Requests": "1"
#         })

#         page = context.new_page()

#         # Step 1: Login
#         page.goto(
#             "https://auth.visas-de.tlscontact.com/auth/realms/atlas/protocol/openid-connect/auth?"
#             "client_id=tlscitizen&redirect_uri=https%3A%2F%2Fvisas-de.tlscontact.com%2Fen-us%2Fauth-callback"
#             "&response_mode=query&response_type=code&scope=openid"
#         )
#         page.fill("input[name='username']", email)
#         page.fill("input[name='password']", password)
#         page.click("button:has-text('Login')")
#         page.wait_for_load_state("networkidle")
#         print("Logged in")

#         try:
#             print("Waiting for country selection...")

#             target_p = page.locator("p.whitespace-nowrap", has_text=country)
#             target_p.wait_for(state="visible", timeout=15000)
#             clickable_card = target_p.locator("..").locator("..")
#             clickable_card.click()
#             print(f"Clicked card containing '{country}'")
#             page.wait_for_timeout(3000)
#         except Exception as e:
#             print("Failed to click country card:", e)

#         # Step 2: Click "Select"
#         # select_btn = page.locator("button:has-text('Select')").nth(1)
#         # select_btn.wait_for(state="visible", timeout=10000)
#         # select_btn.click()
#         # page.wait_for_load_state("networkidle")
#         try:
#             select_btn = page.locator("button:has-text('Select')").nth(1)
#             select_btn.wait_for(state="visible", timeout=10000)
#             select_btn.click()
#             page.wait_for_load_state("networkidle")
#             print("Select button clicked successfully")

#         except TimeoutError:
#             print("❌ Error: 'Select' button not found or not clickable in time")
#             page_text = page.inner_text("body")
#             print("📄 Page Text:\n", page_text)
#             sys.exit(1)

#         except Exception as e:
#             print(f"❌ Unexpected error during Select button click: {e}")
#             page_text = page.inner_text("body")
#             print("📄 Page Text:\n", page_text)
#             sys.exit(1)

#         # Optional: Try clicking "Continue" link if it appears
#         for _ in range(5):
#             try:
#                 continue_btn = page.locator("a:has-text('Continue')")
#                 if continue_btn.count() > 0 and continue_btn.first.is_visible():
#                     continue_btn.first.click()
#                     page.wait_for_load_state("networkidle")
#                     print("Clicked 'Continue' and moved to next step")
#                     break
#                 else:
#                     print("'Continue' button not visible yet. Waiting...")
#                     time.sleep(2)
#             except Exception as e:
#                 print("Retry error while looking for 'Continue':", e)

#         # Step 3: Wait for and click appointment slot
#         wait_for_available_slot_and_click(page)

#         # Step 4: Click "Book your appointment"
#         try:
#             book_btn = page.locator("button:has-text('Book your appointment')")
#             book_btn.wait_for(state="visible", timeout=10000)

#             while book_btn.is_disabled():
#                 print("Waiting for 'Book your appointment' button to enable...")
#                 time.sleep(1)

#             book_btn.click()
#             print("Clicked 'Book your appointment'")

#         except Exception as e:
#             print("Could not click 'Book your appointment':", e)

#         # Step 5: Detect booking confirmation
#         print("Waiting for final confirmation or redirects...")
#         time.sleep(5)

#         try:
#             if page.url.endswith("/confirmation") or "/confirmation" in page.url:
#                 print("Reached confirmation page.")
#             elif page.locator("text=Your appointment has been booked").count() > 0:
#                 print("Appointment confirmed via message.")
#             else:
#                 print("No clear confirmation detected.")
#         except Exception as e:
#             print("Could not verify confirmation:", e)

#         # Step 6: Exit
#         time.sleep(5)
#         browser.close()
#         print("Booking complete. Browser closed. Exiting script.")


# # Run it
# login_and_book()

from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import time
import os
import sys
import random


def random_delay(a=0.5, b=2.0):
    time.sleep(random.uniform(a, b))


def wait_for_available_slot_and_click(page):
    print("⏳ Waiting for standard appointment slot...")
    last_reload_time = time.time()

    while True:
        try:
            page.wait_for_selector("button[data-testid='btn-available-slot']:visible", timeout=5000)
            slot_buttons = page.locator("button[data-testid='btn-available-slot']:visible")
            count = slot_buttons.count()

            if count > 0:
                for i in range(count):
                    button = slot_buttons.nth(i)
                    try:
                        label_span = button.locator("span.sr-only")
                        if label_span.count() == 0:
                            continue

                        label_text = label_span.inner_text().strip().lower()
                        if "standard appointment" in label_text:
                            button.wait_for(state="visible", timeout=3000)
                            time_text = button.inner_text().strip()
                            button.click()
                            print(f"✅ Clicked standard appointment slot: {time_text}")
                            return
                    except Exception as inner_e:
                        print(f"❌ Error inspecting slot {i}: {inner_e}")
                print("❌ No matching 'standard appointment' slot found.")
            else:
                print("❌ No available slot buttons found.")
        except Exception as e:
            print(f"❌ Error during slot lookup: {e}")

        now = time.time()
        elapsed = now - last_reload_time
        print("elapsed time",elapsed)


        print("🔄 Retrying in ~15 seconds...")
        last_reload_time = now 
        time.sleep(random.uniform(13, 17))
        try:
            page.reload(wait_until="domcontentloaded", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as reload_err:
            print(f"⚠️ Error during reload: {reload_err}")


def login_and_book():
    email = os.getenv("BOT_EMAIL")
    password = os.getenv("BOT_PASSWORD")
    country = os.getenv("BOT_COUNTRY")

    if not email or not password or not country:
        print("❌ Missing EMAIL, PASSWORD or COUNTRY environment variable.")
        sys.exit(1)

    ua = UserAgent()
    user_agent = ua.random

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": "http://eu.decodo.com:10000",
                "username": "spkm1bz91s",
                "password": "ybkhaU9Bn+3g1ns4KP"
            }
        )

        context = browser.new_context(
            user_agent=user_agent,
            viewport={"width": random.randint(1200, 1400), "height": random.randint(700, 800)},
            java_script_enabled=True,
            ignore_https_errors=True,
            locale="en-US",
            timezone_id="Europe/London",
            permissions=["geolocation"],
        )

        # Stealth - remove webdriver flag
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
        """)

        # Optional: more stealth-like properties
        # context.add_init_script("""
        #     window.chrome = { runtime: {} };
        #     Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        #     Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        # """)
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            window.chrome = { runtime: {} };
            const originalQuery = navigator.permissions.query;
            navigator.permissions.query = parameters => parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) : originalQuery(parameters);
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.';
            if (parameter === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter(parameter);
            };
        """)


        context.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        })

        page = context.new_page()

        # Step 1: Login
        page.goto(
            "https://auth.visas-de.tlscontact.com/auth/realms/atlas/protocol/openid-connect/auth?"
            "client_id=tlscitizen&redirect_uri=https%3A%2F%2Fvisas-de.tlscontact.com%2Fen-us%2Fauth-callback"
            "&response_mode=query&response_type=code&scope=openid"
        )
        random_delay()
        page.fill("input[name='username']", email)
        random_delay()
        page.fill("input[name='password']", password)
        random_delay()
        page.click("button:has-text('Login')")
        page.wait_for_load_state("networkidle")
        print("✅ Logged in")

        # Step 2: Click country card
        try:
            target_p = page.locator("p.whitespace-nowrap", has_text=country)
            target_p.wait_for(state="visible", timeout=15000)
            clickable_card = target_p.locator("..").locator("..")
            clickable_card.click()
            print(f"🌍 Clicked country: {country}")
            page.wait_for_timeout(2000)
        except Exception as e:
            print("❌ Failed to click country card:", e)

        # Step 3: Click "Select"
        try:
            select_btn = page.locator("button:has-text('Select')").nth(1)
            select_btn.wait_for(state="visible", timeout=10000)
            select_btn.click()
            page.wait_for_load_state("networkidle")
            print("✅ Clicked 'Select' button")
        except Exception as e:
            print("❌ Error during 'Select':", e)
            sys.exit(1)

        # Step 4: Optional "Continue"
        for _ in range(5):
            try:
                continue_btn = page.locator("a:has-text('Continue')")
                if continue_btn.count() > 0 and continue_btn.first.is_visible():
                    continue_btn.first.click()
                    page.wait_for_load_state("networkidle")
                    print("➡️ Clicked 'Continue'")
                    break
                time.sleep(2)
            except Exception:
                pass

        # Step 5: Wait for appointment slot
        wait_for_available_slot_and_click(page)

        # Step 6: Book
        try:
            book_btn = page.locator("button:has-text('Book your appointment')")
            book_btn.wait_for(state="visible", timeout=10000)
            while book_btn.is_disabled():
                print("Waiting for 'Book your appointment' to enable...")
                time.sleep(1)

            book_btn.click()
            print("🎉 Appointment booked!")
        except Exception as e:
            print("❌ Could not click 'Book your appointment':", e)

        # Step 7: Confirmation
        time.sleep(5)
        try:
            if page.url.endswith("/confirmation") or "/confirmation" in page.url:
                print("✅ Confirmation page reached.")
            elif page.locator("text=Your appointment has been booked").count() > 0:
                print("✅ Appointment confirmed.")
            else:
                print("❌ Confirmation unclear.")
        except Exception as e:
            print("❌ Error verifying confirmation:", e)

        browser.close()
        print("🚪 Exiting script.")


# Run the script
login_and_book()

