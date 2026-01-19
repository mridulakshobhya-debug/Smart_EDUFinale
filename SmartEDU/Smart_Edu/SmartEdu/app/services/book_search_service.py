"""
Book Search Service - Uses Groq API to search for books across the internet
"""
import os
import json
import requests
from groq import Groq
from typing import List, Dict, Optional
from urllib.parse import quote

class BookSearchService:
    def __init__(self):
        """Initialize the Book Search Service with Groq API"""
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        
    def search_book_with_groq(self, book_title: str, book_author: str = "") -> Dict:
        """
        Search for a book using Groq API and find the best available source
        
        Args:
            book_title: Title of the book to search for
            book_author: Author of the book (optional)
            
        Returns:
            Dictionary with book info and links
        """
        if not self.client:
            return self._get_fallback_search(book_title, book_author)
        
        try:
            # Create search query
            search_query = f"{book_title}"
            if book_author:
                search_query += f" by {book_author}"
            search_query += " free online read"
            
            # Use Groq to find the best source
            message = self.client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Search for and provide information about this book: {search_query}
                        
Please provide:
1. Exact title
2. Author
3. Best free reading sources (Project Gutenberg, Standard Ebooks, archive.org, Google Books, etc.)
4. Direct links if available
5. Brief description

Format as JSON with keys: title, author, sources (array with name and url), description"""
                    }
                ]
            )
            
            # Parse response
            response_text = message.content[0].text
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    book_data = json.loads(json_str)
                    return book_data
            except json.JSONDecodeError:
                pass
            
            # Fallback: parse response text directly
            return self._parse_groq_response(response_text, book_title, book_author)
            
        except Exception as e:
            print(f"Error searching with Groq: {e}")
            return self._get_fallback_search(book_title, book_author)
    
    def _parse_groq_response(self, response_text: str, book_title: str, book_author: str) -> Dict:
        """Parse Groq response text into structured data"""
        sources = []
        
        # Common book sources
        if "gutenberg" in response_text.lower():
            sources.append({
                "name": "Project Gutenberg",
                "url": f"https://www.gutenberg.org/ebooks/search/?query={quote(book_title)}"
            })
        
        if "archive.org" in response_text.lower() or "internet archive" in response_text.lower():
            sources.append({
                "name": "Internet Archive",
                "url": f"https://archive.org/search.php?query={quote(book_title)}"
            })
        
        if "google books" in response_text.lower():
            sources.append({
                "name": "Google Books",
                "url": f"https://books.google.com/books?q={quote(book_title)}"
            })
        
        if "standard ebooks" in response_text.lower():
            sources.append({
                "name": "Standard Ebooks",
                "url": f"https://standardebooks.org/ebooks/?query={quote(book_title)}"
            })
        
        # Default sources if none found
        if not sources:
            sources = [
                {
                    "name": "Internet Archive",
                    "url": f"https://archive.org/search.php?query={quote(book_title)}"
                },
                {
                    "name": "Google Books",
                    "url": f"https://books.google.com/books?q={quote(book_title)}"
                },
                {
                    "name": "Project Gutenberg",
                    "url": f"https://www.gutenberg.org/ebooks/search/?query={quote(book_title)}"
                }
            ]
        
        return {
            "title": book_title,
            "author": book_author,
            "sources": sources,
            "description": response_text[:300]
        }
    
    def _get_fallback_search(self, book_title: str, book_author: str = "") -> Dict:
        """Provide fallback search results when Groq is not available"""
        sources = [
            {
                "name": "Internet Archive",
                "url": f"https://archive.org/search.php?query={quote(book_title)}"
            },
            {
                "name": "Google Books",
                "url": f"https://books.google.com/books?q={quote(book_title)}"
            },
            {
                "name": "Project Gutenberg",
                "url": f"https://www.gutenberg.org/ebooks/search/?query={quote(book_title)}"
            },
            {
                "name": "Standard Ebooks",
                "url": f"https://standardebooks.org/ebooks/?query={quote(book_title)}"
            },
            {
                "name": "Open Library",
                "url": f"https://openlibrary.org/search?q={quote(book_title)}"
            }
        ]
        
        return {
            "title": book_title,
            "author": book_author,
            "sources": sources,
            "description": f"Search results for '{book_title}' across multiple free book sources"
        }
    
    def get_all_books_search_suggestions(self) -> List[Dict]:
        """
        Get a list of popular books to display in the library
        Returns a curated list of classic and popular books
        """
        popular_books = [
            {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Classics"},
            {"title": "1984", "author": "George Orwell", "category": "Classics"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classics"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classics"},
            {"title": "Jane Eyre", "author": "Charlotte Brontë", "category": "Classics"},
            {"title": "Wuthering Heights", "author": "Emily Brontë", "category": "Classics"},
            {"title": "Moby Dick", "author": "Herman Melville", "category": "Adventure"},
            {"title": "The Odyssey", "author": "Homer", "category": "Classics"},
            {"title": "The Adventures of Sherlock Holmes", "author": "Arthur Conan Doyle", "category": "Mystery"},
            {"title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll", "category": "Fantasy"},
            {"title": "Frankenstein", "author": "Mary Shelley", "category": "Classics"},
            {"title": "Dracula", "author": "Bram Stoker", "category": "Horror"},
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"},
            {"title": "A Tale of Two Cities", "author": "Charles Dickens", "category": "Classics"},
            {"title": "Dune", "author": "Frank Herbert", "category": "Science Fiction"},
            {"title": "Foundation", "author": "Isaac Asimov", "category": "Science Fiction"},
            {"title": "Neuromancer", "author": "William Gibson", "category": "Cyberpunk"},
            {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "category": "Fantasy"},
            {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "category": "Fantasy"},
            {"title": "Atomic Habits", "author": "James Clear", "category": "Self-Help"},
        ]
        
        return popular_books
    
    def search_and_redirect(self, book_title: str, book_author: str = "") -> str:
        """
        Search for a book and return the best available read-now link
        """
        book_data = self.search_book_with_groq(book_title, book_author)
        
        # Return the first available source URL
        if book_data.get("sources") and len(book_data["sources"]) > 0:
            return book_data["sources"][0]["url"]
        
        # Fallback to generic search
        return f"https://archive.org/search.php?query={quote(book_title)}"
