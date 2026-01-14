
from playwright.sync_api import sync_playwright
import os
import re

def generate_icons():
    # Read the source SVG
    with open('favicon.svg', 'r') as f:
        svg_content = f.read()

    # Create a version for Apple Touch Icon (Square corners)
    # Remove rx="8" to make it square
    # We use regex to find rx="8" and remove it, or set rx="0"
    square_svg = re.sub(r'rx="\d+"', 'rx="0"', svg_content)

    # Create a temporary HTML file to render this modified SVG
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body, html {{ margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; background: white; }}
            #icon {{ width: 180px; height: 180px; }}
            svg {{ width: 100%; height: 100%; }}
        </style>
    </head>
    <body>
        <div id="icon">
            {square_svg}
        </div>
    </body>
    </html>
    """

    with open('scripts/temp_renderer.html', 'w') as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"file://{os.path.abspath('scripts/temp_renderer.html')}"
        page.goto(url)

        # Select the SVG element
        svg_element = page.locator("#icon svg")

        # Take a screenshot
        svg_element.screenshot(path="apple-touch-icon.png", omit_background=True)

        browser.close()

    # Cleanup
    if os.path.exists('scripts/temp_renderer.html'):
        os.remove('scripts/temp_renderer.html')

if __name__ == "__main__":
    generate_icons()
