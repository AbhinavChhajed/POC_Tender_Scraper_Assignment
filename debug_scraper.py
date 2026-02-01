from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating to nprocure...")
        page.goto("https://tender.nprocure.com/")
        page.wait_for_timeout(5000) # Wait 5s for everything to load
        
        # Save the HTML to a file
        content = page.content()
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved HTML to 'debug_page.html'. Open it to check the structure.")
        browser.close()

if __name__ == "__main__":
    run()