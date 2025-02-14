import os
import pickle
import faiss
import numpy as np
from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer


app = Flask(__name__)


model = SentenceTransformer('all-MiniLM-L6-v2')


embedding_file = 'song_embeddings.pkl'
faiss_index_file = 'faiss_index.bin'

if not os.path.exists(embedding_file):
    raise FileNotFoundError(f" {embedding_file} not found. Make sure to generate it first.")

with open(embedding_file, 'rb') as f:
    song_embeddings = pickle.load(f)


embeddings = np.array([song["embedding"] for song in song_embeddings])


if os.path.exists(faiss_index_file):
    print("Loading FAISS index from file...")
    index = faiss.read_index(faiss_index_file)
else:
    print(" Creating FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])  
    index.add(embeddings)
    faiss.write_index(index, faiss_index_file)  
    print("FAISS index saved.")

print("FAISS Index Type:", type(index))  

def distance_to_similarity(distance):
    return 1 / (1 + distance)

def find_similar_songs(query_lyrics, k=5):
    query_embedding = model.encode([query_lyrics], convert_to_numpy=True)

    print("DEBUG: Type of index before search:", type(index)) 

    D, I = index.search(query_embedding, k) 
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
