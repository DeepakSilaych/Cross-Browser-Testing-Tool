#!/usr/bin/env python3
import argparse
import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from PIL import Image, ImageChops
from playwright.async_api import async_playwright
from jinja2 import Template

class CrossBrowserTester:
    def __init__(self, url: str, browsers: List[str], headless: bool = True):
        self.url = url
        self.browsers = browsers
        self.headless = headless
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        
    async def capture_screenshots(self) -> Dict[str, str]:
        screenshots = {}
        async with async_playwright() as p:
            for browser_name in self.browsers:
                try:
                    browser = await getattr(p, browser_name).launch(headless=self.headless)
                    page = await browser.new_page()
                    
                    # Set viewport size
                    await page.set_viewport_size({"width": 1280, "height": 800})
                    
                    # Navigate and wait for network idle
                    await page.goto(self.url, wait_until="networkidle")
                    
                    # Capture full page screenshot
                    screenshot_path = self.results_dir / f"{browser_name}.png"
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    screenshots[browser_name] = str(screenshot_path)
                    
                    await browser.close()
                except Exception as e:
                    print(f"Error capturing {browser_name}: {str(e)}")
        
        return screenshots

    def compare_screenshots(self, screenshots: Dict[str, str]) -> Dict[str, float]:
        if not screenshots:
            return {}

        # Use first browser as baseline
        baseline_browser = list(screenshots.keys())[0]
        baseline_img = Image.open(screenshots[baseline_browser])
        
        differences = {}
        for browser, screenshot in screenshots.items():
            if browser == baseline_browser:
                continue
                
            test_img = Image.open(screenshot)
            
            # Ensure images are the same size
            if baseline_img.size != test_img.size:
                test_img = test_img.resize(baseline_img.size)
            
            # Calculate difference
            diff = ImageChops.difference(baseline_img, test_img)
            diff_path = self.results_dir / f"diff_{baseline_browser}_{browser}.png"
            diff.save(str(diff_path))
            
            # Calculate percentage difference
            diff_pixels = sum(1 for pixel in diff.getdata() if sum(pixel) > 0)
            total_pixels = baseline_img.size[0] * baseline_img.size[1]
            difference_percentage = (diff_pixels / total_pixels) * 100
            differences[browser] = difference_percentage
            
        return differences

    def generate_report(self, screenshots: Dict[str, str], differences: Dict[str, float]):
        with open('template.html', 'r') as f:
            template_str = f.read()
        
        template = Template(template_str)
        baseline_browser = list(screenshots.keys())[0]
        
        html = template.render(
            url=self.url,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            screenshots=screenshots,
            differences=differences,
            baseline_browser=baseline_browser
        )
        
        with open(self.results_dir / "report.html", "w") as f:
            f.write(html)

async def main():
    parser = argparse.ArgumentParser(description="Cross Browser Testing Tool")
    parser.add_argument("--url", required=True, help="Website URL to test")
    parser.add_argument("--browsers", default="chromium,firefox", help="Comma-separated list of browsers")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    
    args = parser.parse_args()
    browsers = [b.strip() for b in args.browsers.split(",")]
    
    tester = CrossBrowserTester(args.url, browsers, args.headless)
    
    print(f"Testing {args.url} in browsers: {', '.join(browsers)}")
    screenshots = await tester.capture_screenshots()
    
    if screenshots:
        print("\nComparing screenshots...")
        differences = tester.compare_screenshots(screenshots)
        
        print("\nGenerating report...")
        tester.generate_report(screenshots, differences)
        
        print(f"\nResults saved in {tester.results_dir}/")
    else:
        print("No screenshots were captured. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
