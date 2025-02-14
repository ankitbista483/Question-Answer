from sentence_transformers import SentenceTransformer
import pandas as pd
import pickle
import faiss
import numpy as np
import os

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# File paths
csv_path = "/Users/ankitbista/Desktop/practice/Question-Answer/song_lyrics_cleaned.csv"
pkl_path = "song_embeddings.pkl"
faiss_index_path = "faiss_index.bin"

# Load or create song embeddings
if os.path.exists(pkl_path):
    with open(pkl_path, "rb") as f:
        song_embeddings = pickle.load(f)
    print("✅ Loaded song embeddings from file.")
else:
    df = pd.read_csv(csv_path)
    print("🔄 Generating song embeddings...")

    # Batch encoding for efficiency
    embeddings = model.encode(df["Lyrics"].tolist(), convert_to_numpy=True)
    song_embeddings = [{"Song Title": title, "embedding": emb} for title, emb in zip(df["Song Title"], embeddings)]
    
    # Save embeddings
    with open(pkl_path, "wb") as f:
        pickle.dump(song_embeddings, f)
    print("✅ Saved song embeddings.")

# Convert embeddings to NumPy array
embeddings = np.array([song["embedding"] for song in song_embeddings])

# Load or create FAISS index
if os.path.exists(faiss_index_path):
    index = faiss.read_index(faiss_index_path)
    print("✅ Loaded FAISS index from file.")
else:
    print("🔄 Creating FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, faiss_index_path)
    print("✅ Saved FAISS index.")

def distance_to_similarity(distance):
    """Convert FAISS L2 distance to a similarity score."""
    return 1 / (1 + distance)

def find_closest_songs(query_lyrics, top_k=5):
    """Find the most similar songs based on lyrics."""
    query_embedding = model.encode([query_lyrics], convert_to_numpy=True)
    D, I = index.search(query_embedding, top_k)  
    closest_songs = [(song_embeddings[I[0][i]]["Song Title"], distance_to_similarity(D[0][i])) for i in range(top_k)]
    return closest_songs

# Test the function
query_lyrics = "imma pull up in a bentley with a fuckin 100 thou in my pocket"
top_5_songs = find_closest_songs(query_lyrics)

print("\n🔍 **Top 5 Similar Songs:**")
for song, similarity_score in top_5_songs:
    print(f"🎵 {song} | 🔥 Similarity: {similarity_score:.4f}")
