import json
import faiss

def save_index(index, index_path):
    faiss.write_index(index, index_path)

def load_index(index_path):
    return faiss.read_index(index_path)

def save_metadata(metadata, path):
    with open(path, "w") as f:
        json.dump(metadata, f)

def load_metadata(path):
    with open(path, "r") as f:
        return json.load(f)