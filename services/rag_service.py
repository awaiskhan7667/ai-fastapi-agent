from sentence_transformers import SentenceTransformer
from openai import OpenAI
from config import settings
import faiss
import numpy as np
from pypdf import PdfReader

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = OpenAI(api_key=settings.openai_api_key)


def load_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def load_and_split_pdf(file_path):
    text = load_pdf(file_path)

    chunks = split_text(
        text,
        chunk_size=500,
        overlap=50
    )

    return chunks

def build_pdf_index(file_path):
    chunks = load_and_split_pdf(file_path)

    embeddings = create_embeddings(chunks)

    index = create_vector_index(embeddings)

    return index, chunks

def load_document(text: str):
    return text

def pdf_rag_answer(question, file_path):
    index, chunks = build_pdf_index(file_path)

    return rag_answer(
        question,
        index,
        chunks
    )

def split_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks

def create_embeddings(chunks):
    embeddings = embedding_model.encode(chunks)

    return np.array(embeddings).astype("float32")

def create_vector_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def build_index(chunks):
    embeddings = create_embeddings(chunks)
    index = create_vector_index(embeddings)

    return index, chunks

def search_chunks(query, index, chunks, top_k=3, threshold=1.0):
    query_embedding = create_embeddings([query])

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, i in zip(distances[0], indices[0]):
        if distance <= threshold:
            results.append(chunks[i])

    return results

def generate_rag_answer(question, context):
    prompt = f"""
You are a RAG assistant.

Answer the question using ONLY the context below.

If the answer cannot be found in the context,
say: "I don't know based on the provided document."

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text

def rag_answer(question, index, chunks):
    relevant_chunks = search_chunks(
        question,
        index,
        chunks
    )

    if not relevant_chunks:
        return "I don't know based on the provided document."

    context = "\n\n".join(relevant_chunks)

    return generate_rag_answer(question, context)



if __name__ == "__main__":
    answer = pdf_rag_answer("give me the list of the skills?", "documents/Profile.pdf")

    print("Answer:", answer)