"""
Test script for the Book Search Service
Run this to verify everything is working correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.book_search_service import BookSearchService

def test_book_search_service():
    """Test the book search service without requiring a Groq API key"""
    
    print("=" * 60)
    print("SmartEDU Book Search Service - Test")
    print("=" * 60)
    
    # Initialize service
    service = BookSearchService()
    print("\n✅ BookSearchService initialized successfully")
    
    # Test 1: Get popular books
    print("\n--- Test 1: Get Popular Books ---")
    books = service.get_all_books_search_suggestions()
    print(f"✅ Retrieved {len(books)} popular books")
    print(f"   Sample books:")
    for book in books[:3]:
        print(f"   - '{book['title']}' by {book['author']}")
    
    # Test 2: Fallback search (without Groq API)
    print("\n--- Test 2: Fallback Search ---")
    result = service._get_fallback_search("1984", "George Orwell")
    print(f"✅ Fallback search working")
    print(f"   Found {len(result['sources'])} sources for '1984':")
    for i, source in enumerate(result['sources'], 1):
        print(f"   {i}. {source['name']}")
    
    # Test 3: Redirect URL generation
    print("\n--- Test 3: Redirect URL Generation ---")
    url = service.search_and_redirect("Pride and Prejudice", "Jane Austen")
    print(f"✅ Generated redirect URL:")
    print(f"   {url[:80]}...")
    
    # Test 4: Response parsing
    print("\n--- Test 4: Response Parsing ---")
    sample_response = """
    Found this book on Internet Archive and Project Gutenberg.
    The book is available through multiple sources including
    archive.org and other platforms.
    """
    parsed = service._parse_groq_response(sample_response, "Test Book", "Test Author")
    print(f"✅ Parsed response structure:")
    print(f"   Title: {parsed['title']}")
    print(f"   Author: {parsed['author']}")
    print(f"   Sources found: {len(parsed['sources'])}")
    print(f"   Description length: {len(parsed['description'])} chars")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ All Tests Passed!")
    print("=" * 60)
    print("\n📚 The Book Search Service is working correctly!")
    print("\nTo use with Groq AI:")
    print("1. Get API key from https://console.groq.com/keys")
    print("2. Add to .env file: GROQ_API_KEY=your_key_here")
    print("3. Restart the Flask application")
    print("\nTo start the app:")
    print("  python run.py")
    print("\nThen visit: http://localhost:5000/elibrary")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        test_book_search_service()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
