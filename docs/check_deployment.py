#!/usr/bin/env python3
"""
Script to verify GitHub Pages deployment for PyP6Xer documentation.
"""

import requests
import time
import sys

def check_github_pages(url, max_retries=10, delay=30):
    """Check if GitHub Pages site is accessible."""
    print(f"Checking GitHub Pages deployment at: {url}")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Success! Documentation is live at {url}")
                print(f"Response status: {response.status_code}")
                return True
            else:
                print(f"❌ Attempt {attempt + 1}: Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt + 1}: Error - {e}")
        
        if attempt < max_retries - 1:
            print(f"Waiting {delay} seconds before next attempt...")
            time.sleep(delay)
    
    print(f"❌ Failed to access {url} after {max_retries} attempts")
    return False

def check_key_pages(base_url):
    """Check if key documentation pages are accessible."""
    key_pages = [
        "",  # Main page
        "getting_started.html",
        "examples.html",
        "api/xerparser/index.html",
        "contributing.html"
    ]
    
    results = {}
    for page in key_pages:
        url = f"{base_url}/{page}".rstrip('/')
        try:
            response = requests.get(url, timeout=10)
            results[page or "index"] = response.status_code == 200
            print(f"{'✅' if response.status_code == 200 else '❌'} {page or 'index'}: {response.status_code}")
        except Exception as e:
            results[page or "index"] = False
            print(f"❌ {page or 'index'}: Error - {e}")
    
    return results

if __name__ == "__main__":
    github_pages_url = "https://hassanemam.github.io/PyP6Xer"
    
    print("PyP6Xer Documentation Deployment Checker")
    print("=" * 50)
    
    # Check main site
    if check_github_pages(github_pages_url):
        print("\n" + "=" * 50)
        print("Checking key documentation pages...")
        results = check_key_pages(github_pages_url)
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"\nSummary: {success_count}/{total_count} pages accessible")
        
        if success_count == total_count:
            print("🎉 All documentation pages are working correctly!")
            sys.exit(0)
        else:
            print("⚠️  Some pages may need attention")
            sys.exit(1)
    else:
        print("❌ GitHub Pages site is not accessible yet")
        print("This might be normal if the workflow just completed.")
        print("GitHub Pages can take a few minutes to propagate changes.")
        sys.exit(1)
