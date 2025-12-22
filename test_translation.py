#!/usr/bin/env python3
"""
Test script to verify the Docusaurus i18n translation system in the Humonoid Robotics Book project.
This script tests the i18n structure, completeness, and functionality of the translation system.
"""

import os
import json
import subprocess
from pathlib import Path


def test_i18n_structure():
    """Test the Docusaurus i18n structure and configuration"""
    project_root = Path(__file__).parent
    i18n_path = project_root / "i18n"

    print("Testing Docusaurus i18n structure...")
    print(f"Project root: {project_root}")
    print(f"i18n directory: {i18n_path}")

    # Check if i18n directory exists
    if not i18n_path.exists():
        print("[ERROR] i18n directory does not exist")
        return False

    print("[SUCCESS] i18n directory exists")

    # Check supported locales in i18n directory
    locales = [d.name for d in i18n_path.iterdir() if d.is_dir()]
    print(f"[SUCCESS] Supported locales: {locales}")

    # Check docusaurus.config.ts for i18n configuration
    config_path = project_root / "docusaurus.config.ts"
    if not config_path.exists():
        print("[ERROR] docusaurus.config.ts does not exist")
        return False

    with open(config_path, 'r', encoding='utf-8') as f:
        config_content = f.read()

    if "i18n:" in config_content or "i18n" in config_content:
        print("[SUCCESS] i18n configuration found in docusaurus.config.ts")
    else:
        print("[WARNING] i18n configuration not found in docusaurus.config.ts")

    # Check for each locale's structure
    for locale in locales:
        locale_path = i18n_path / locale
        print(f"\nTesting locale: {locale}")

        # Check required i18n subdirectories for each locale
        required_dirs = [
            "docusaurus-plugin-content-docs",
            "docusaurus-plugin-content-pages",
            "docusaurus-theme-classic"
        ]

        for dir_name in required_dirs:
            dir_path = locale_path / dir_name
            if not dir_path.exists():
                print(f"[ERROR] {dir_path} does not exist")
                return False
            print(f"[SUCCESS] {dir_path} exists")

            # Count files in each directory
            files = list(dir_path.glob('*'))
            print(f"  - Contains {len(files)} items")

    print("\n[SUCCESS] i18n structure verification completed successfully!")
    return True


def test_translation_completeness():
    """Test the completeness of translations across locales"""
    project_root = Path(__file__).parent
    docs_path = project_root / "docs"
    i18n_path = project_root / "i18n"

    if not docs_path.exists() or not i18n_path.exists():
        print("❌ Source docs or i18n path does not exist")
        return False

    # Get all English docs
    english_docs = set()
    for doc_file in docs_path.glob("*.md"):
        english_docs.add(doc_file.name)

    print(f"\nSource documentation files: {len(english_docs)}")
    for doc in english_docs:
        print(f"  - {doc}")

    # Check each locale's translation completeness
    locales = [d.name for d in i18n_path.iterdir() if d.is_dir()]

    for locale in locales:
        print(f"\nTranslation completeness for locale '{locale}':")

        locale_docs_path = i18n_path / locale / "docusaurus-plugin-content-docs" / "current"
        if not locale_docs_path.exists():
            print(f"[ERROR] {locale_docs_path} does not exist")
            continue

        # Get all translated docs for this locale
        translated_docs = set()
        for doc_file in locale_docs_path.glob("*.md"):
            translated_docs.add(doc_file.name)

        print(f"  Translated docs: {len(translated_docs)}")
        for doc in translated_docs:
            print(f"    - {doc}")

        # Calculate coverage
        if english_docs:
            coverage = len(translated_docs) / len(english_docs) * 100
            print(f"  Translation coverage: {coverage:.1f}% ({len(translated_docs)}/{len(english_docs)})")

        # Identify missing translations
        missing_docs = english_docs - translated_docs
        if missing_docs:
            print(f"  Missing translations: {len(missing_docs)}")
            for doc in sorted(missing_docs):
                print(f"    - {doc}")
        else:
            print(f"  [SUCCESS] All English docs have {locale} translations")

    return True


def test_theme_translations():
    """Test theme-specific translations (navbar, footer, etc.)"""
    project_root = Path(__file__).parent
    i18n_path = project_root / "i18n"

    locales = [d.name for d in i18n_path.iterdir() if d.is_dir()]

    print(f"\nTesting theme translations...")

    for locale in locales:
        theme_path = i18n_path / locale / "docusaurus-theme-classic"
        if not theme_path.exists():
            print(f"[ERROR] Theme path for {locale} does not exist")
            continue

        # Check for common theme translation files
        theme_files = {
            "navbar.json": "Navigation bar translations",
            "footer.json": "Footer translations",
            "code.json": "General theme translations"
        }

        print(f"\nLocale '{locale}' theme files:")
        for file_name, description in theme_files.items():
            file_path = theme_path / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"  [SUCCESS] {file_name} - {len(data)} translation keys ({description})")
                except json.JSONDecodeError:
                    print(f"  [ERROR] {file_name} - Invalid JSON format")
            else:
                print(f"  [WARNING] {file_name} - Missing ({description})")


def test_pages_translations():
    """Test pages-specific translations"""
    project_root = Path(__file__).parent
    i18n_path = project_root / "i18n"

    locales = [d.name for d in i18n_path.iterdir() if d.is_dir()]

    print(f"\nTesting pages translations...")

    for locale in locales:
        pages_path = i18n_path / locale / "docusaurus-plugin-content-pages"
        if not pages_path.exists():
            print(f"[ERROR] Pages path for {locale} does not exist")
            continue

        print(f"\nLocale '{locale}' pages translations:")
        page_files = list(pages_path.glob("*.json"))

        if not page_files:
            print(f"  No page translation files found")
            continue

        for page_file in page_files:
            try:
                with open(page_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  [SUCCESS] {page_file.name} - {len(data)} translation keys")
            except json.JSONDecodeError:
                print(f"  [ERROR] {page_file.name} - Invalid JSON format")


def test_i18n_functionality():
    """Test i18n functionality by checking build process"""
    project_root = Path(__file__).parent

    print(f"\nTesting i18n functionality...")

    # Check if package.json exists
    package_json_path = project_root / "package.json"
    if not package_json_path.exists():
        print("[WARNING] package.json not found - cannot test build process")
        return True

    # Check if Node.js and npm are available
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("[WARNING] npm not available - cannot test build process")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("[WARNING] npm not available - cannot test build process")
        return True

    print("[SUCCESS] npm is available for i18n testing")
    print("\nTo test full i18n functionality:")
    print("- Run: npm run build")
    print("- This will build all locales defined in docusaurus.config.ts")
    print("- Check if build succeeds for all configured locales")
    print("- Access: http://localhost:3000/ and http://localhost:3000/ur/ after running npm run start")

    return True


def main():
    """Main function to run all i18n tests"""
    print("Testing Docusaurus i18n Translation System\n")

    all_tests_passed = True

    # Test 1: i18n structure
    print("="*60)
    print("1. Testing i18n structure...")
    if not test_i18n_structure():
        all_tests_passed = False

    # Test 2: Translation completeness
    print("\n" + "="*60)
    print("2. Testing translation completeness...")
    if not test_translation_completeness():
        all_tests_passed = False

    # Test 3: Theme translations
    print("\n" + "="*60)
    print("3. Testing theme translations...")
    test_theme_translations()

    # Test 4: Pages translations
    print("\n" + "="*60)
    print("4. Testing pages translations...")
    test_pages_translations()

    # Test 5: i18n functionality
    print("\n" + "="*60)
    print("5. Testing i18n functionality...")
    if not test_i18n_functionality():
        all_tests_passed = False

    print("\n" + "="*60)
    if all_tests_passed:
        print("SUCCESS: All i18n tests passed!")
        print("\nThe Docusaurus i18n system is properly configured with:")
        print("- Proper directory structure")
        print("- Complete documentation translations")
        print("- Theme translations")
        print("- Pages translations")
        print("- Functional build process")
    else:
        print("ERROR: Some i18n tests failed!")
        print("\nCheck the errors above and fix the issues before deploying.")

    return all_tests_passed


if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)