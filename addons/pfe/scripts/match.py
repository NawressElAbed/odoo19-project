import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def run_match(cv_texts, job_texts):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    cv_embeddings = model.encode(cv_texts, convert_to_tensor=True)
    job_embeddings = model.encode(job_texts, convert_to_tensor=True)

    similarity_scores = cosine_similarity(cv_embeddings.cpu(), job_embeddings.cpu())

    preselection = []
    for i in range(similarity_scores.shape[0]):
        for j in range(similarity_scores.shape[1]):
            preselection.append({
                "CV_index": i,
                "Job_index": j,
                "Score": similarity_scores[i, j]
            })

    return preselection, similarity_scores
