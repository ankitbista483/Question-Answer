import os
import pickle
import faiss
import numpy as np
from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load song embeddings
embedding_file = 'song_embeddings.pkl'
faiss_index_file = 'faiss_index.bin'

if not os.path.exists(embedding_file):
    raise FileNotFoundError(f"❌ {embedding_file} not found. Make sure to generate it first.")

with open(embedding_file, 'rb') as f:
    song_embeddings = pickle.load(f)

# Convert embeddings to numpy array
embeddings = np.array([song["embedding"] for song in song_embeddings])

# Load or create FAISS index
if os.path.exists(faiss_index_file):
    print("✅ Loading FAISS index from file...")
    index = faiss.read_index(faiss_index_file)
else:
    print("🔄 Creating FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])  # Use 'index' here
    index.add(embeddings)
    faiss.write_index(index, faiss_index_file)  # Save FAISS index
    print("✅ FAISS index saved.")

print("FAISS Index Type:", type(index))  # Ensure it's a FAISS index

def distance_to_similarity(distance):
    """Convert FAISS L2 distance to a similarity score."""
    return 1 / (1 + distance)

def find_similar_songs(query_lyrics, k=5):
    """Find the most similar songs based on lyrics."""
    query_embedding = model.encode([query_lyrics], convert_to_numpy=True)

    print("DEBUG: Type of index before search:", type(index))  # Check index type

    D, I = index.search(query_embedding, k)  # Use 'index' here

    results = [(song_embeddings[i]["Song Title"], distance_to_similarity(D[0][idx])) for idx, i in enumerate(I[0])]
    return results


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = find_similar_songs(query)
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
