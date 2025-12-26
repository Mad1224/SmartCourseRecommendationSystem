from app import create_app
from database.mongo import mongo
from ml.evaluation import precision_at_k, hit_rate_at_k
from ml.hybrid_recommender import (
    compute_content_similarity,
    compute_feedback_scores,
    hybrid_score
)
from ml.tfidf_cache import tfidf_matrix, vectorizer
from ml.preprocessing import preprocess_text
from ml.course_cache import get_courses
import numpy as np

K = 3
RELEVANCE_THRESHOLD = 4  # rating >= 4 is relevant

app = create_app()

with app.app_context():
    users = list(mongo.db.users.find())

    precision_scores = []
    hit_rates = []

    for user in users:
        user_id = str(user["_id"])

        feedback = list(mongo.db.feedback.find({"user_id": user_id}))
        if not feedback:
            continue

        # Relevant courses (ground truth)
        relevant_course_ids = [
            fb["course_code"]
            for fb in feedback
            if fb.get("rating", 0) >= RELEVANCE_THRESHOLD
        ]

        if not relevant_course_ids:
            continue

        # Use feedback comments as query proxy
        query_text = " ".join([fb.get("comment", "") for fb in feedback])
        cleaned = preprocess_text(query_text)
        query_vec = vectorizer.transform([cleaned])

        courses = get_courses()
        course_ids = [c["course_code"] for c in courses]

        content_scores = compute_content_similarity(tfidf_matrix, query_vec)
        feedback_scores = compute_feedback_scores(
            course_ids,
            feedback
        )

        final_scores = hybrid_score(
            content_scores,
            feedback_scores,
            num_feedback=len(feedback)
        )

        ranked_indices = np.argsort(final_scores)[::-1]
        recommended_ids = [course_ids[i] for i in ranked_indices]

        precision_scores.append(
            precision_at_k(recommended_ids, relevant_course_ids, K)
        )
        hit_rates.append(
            hit_rate_at_k(recommended_ids, relevant_course_ids, K)
        )

    print("===== EVALUATION RESULTS =====")
    print(f"Precision@{K}: {sum(precision_scores)/len(precision_scores):.3f}")
    print(f"Hit Rate@{K}: {sum(hit_rates)/len(hit_rates):.3f}")



##from ml.evaluation import precision_at_k, recall_at_k
#from ml.hybrid_recommender import hybrid_recommend
##from database.mongo import mongo
#from app import create_app

#app = create_app()

#with app.app_context():
 #   users = mongo.db.users.find()
#
 #   K = 5
#
 #   for user in users:
  #      user_id = str(user["_id"])
#
 #       # Get user feedback (ground truth)
  #      feedback = mongo.db.feedback.find({"user_id": user_id})
   #     relevant_courses = [
    #        f["course_id"] for f in feedback if f.get("rating", 0) >= 4
      #  ]

    #    if not relevant_courses:
    #        continue

        # Run hybrid recommendation
     #   results = hybrid_recommend(
#            query="data science machine learning",
 #           user_id=user_id
     #   )

#        recommended = [r["course"] for r in results]

 #       p_k = precision_at_k(recommended, relevant_courses, K)
  #      r_k = recall_at_k(recommended, relevant_courses, K)

   #     print(f"User {user_id}")
    #    print(f"Precision@{K}: {p_k:.2f}")
     #   print(f"Recall@{K}: {r_k:.2f}")
    #    print("-" * 30)

