from flask import Flask, render_template, request, jsonify
from es import es
from flask_cors import CORS
import os
import re
from html.parser import HTMLParser

app = Flask(__name__, template_folder='templates')
CORS(app)

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_text(self):
        return ''.join(self.text)

def strip_html(html):
    """Remove HTML tags and clean up whitespace"""
    if not html:
        return ""
    
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    stripper = HTMLStripper()
    try:
        stripper.feed(html)
        text = stripper.get_text()
    except:
        text = html
    
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_title(source):
    """Extract title from various possible fields"""
    title = source.get('title', '') or source.get('h1', '') or source.get('og:title', '')
    if title:
        return title.strip()
    return 'Untitled'

def extract_snippet(source):
    """Extract and clean snippet from content"""
    text = source.get('snippet', '') or source.get('description', '') or source.get('content', '')
    
    text = strip_html(text)
    
    if len(text) > 200:
        text = text[:197] + '...'
    
    return text if text else 'No preview available'

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').strip()
    
    if not query:
        return jsonify({'results': [], 'error': None})
    
    try:
        results = es.search(
            index="search_engine",
            body={
                "query": {"match": {"content": query}},
                "size": 10,
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 150,
                            "number_of_fragments": 1
                        }
                    }
                }
            }
        )
        
        hits = []
        for hit in results['hits']['hits']:
            source = hit['_source']
            
            if 'highlight' in hit and hit['highlight'].get('content'):
                snippet = strip_html(hit['highlight']['content'][0])
            else:
                snippet = extract_snippet(source)
            
            hits.append({
                'url': source.get('url', ''),
                'score': hit['_score'],
                'title': extract_title(source),
                'snippet': snippet
            })
        
        return jsonify({
            'results': hits,
            'error': None
        })
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({
            'results': [],
            'error': f"Search failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

