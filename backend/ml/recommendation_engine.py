"""
Unified Recommendation Engine
Combines content-based, collaborative filtering, and hybrid recommendations
"""
import joblib
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import preprocess_text

class RecommendationEngine:
    """
    Main recommendation engine that handles:
    - TF-IDF model loading
    - Content-based recommendations
    - Collaborative filtering
    - Hybrid recommendations
    - Model evaluation
    """
    
    def __init__(self, artifacts_path="ml/artifacts"):
        self.artifacts_path = artifacts_path
        self.vectorizer = None
        self.tfidf_matrix = None
        self.is_loaded = False
        
    def load_models(self):
        """Load TF-IDF models from disk"""
        try:
            vectorizer_path = os.path.join(self.artifacts_path, "tfidf_vectorizer.pkl")
            matrix_path = os.path.join(self.artifacts_path, "course_tfidf_matrix.pkl")
            
            if not os.path.exists(vectorizer_path):
                print(f"❌ Vectorizer not found at: {vectorizer_path}")
                return False
                
            if not os.path.exists(matrix_path):
                print(f"❌ TF-IDF matrix not found at: {matrix_path}")
                return False
            
            self.vectorizer = joblib.load(vectorizer_path)
            self.tfidf_matrix = joblib.load(matrix_path)
            self.is_loaded = True
            
            print(f"✅ Loaded TF-IDF models")
            print(f"   Vocabulary size: {len(self.vectorizer.vocabulary_)}")
            print(f"   Matrix shape: {self.tfidf_matrix.shape}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.is_loaded = False
            return False
    
    def reload_models(self):
        """Reload models (useful after rebuilding)"""
        return self.load_models()
    
    def compute_content_similarity(self, user_query):
        """
        Compute content-based similarity scores using TF-IDF
        
        Args:
            user_query: String containing user interests/preferences
            
        Returns:
            numpy array of similarity scores for all courses
        """
        if not self.is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        # Preprocess and vectorize user query
        cleaned_query = preprocess_text(user_query)
        query_vector = self.vectorizer.transform([cleaned_query])
        
        # Compute cosine similarity
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        return similarity_scores
    
    def compute_collaborative_scores(self, course_codes, feedback_docs):
        """
        Compute collaborative filtering scores based on user feedback
        
        Args:
            course_codes: List of course codes in order (matching courses)
            feedback_docs: List of feedback documents from MongoDB
            
        Returns:
            numpy array of collaborative scores (normalized 0-1)
        """
        # Initialize scores for all courses
        scores = {code: 0.0 for code in course_codes}
        counts = {code: 0 for code in course_codes}
        
        # Aggregate ratings from feedback
        for feedback in feedback_docs:
            course_code = feedback.get("course_code")
            rating = feedback.get("rating", 0)
            
            if course_code in scores:
                scores[course_code] += rating
                counts[course_code] += 1
        
        # Calculate average ratings and normalize to 0-1 range
        for code in scores:
            if counts[code] > 0:
                avg_rating = scores[code] / counts[code]
                scores[code] = avg_rating / 5.0  # Normalize (assuming 5-star scale)
        
        # Return as numpy array in the same order as course_codes
        return np.array([scores[code] for code in course_codes])
    
    def adaptive_alpha(self, num_feedback, min_alpha=0.3, max_alpha=0.9):
        """
        Calculate adaptive weight for content-based vs collaborative filtering
        
        Args:
            num_feedback: Number of feedback entries available
            min_alpha: Minimum weight for content (when lots of feedback)
            max_alpha: Maximum weight for content (when no feedback)
            
        Returns:
            alpha value between min_alpha and max_alpha
        """
        if num_feedback == 0:
            return max_alpha  # Pure content-based
        elif num_feedback < 5:
            return 0.8  # Mostly content
        elif num_feedback < 20:
            return 0.6  # Balanced
        else:
            return min_alpha  # More collaborative
    
    def hybrid_recommend(self, user_query, course_codes, feedback_docs, alpha=None):
        """
        Generate hybrid recommendations combining content and collaborative filtering
        
        Args:
            user_query: User interests as text
            course_codes: List of course codes (in order matching TF-IDF matrix)
            feedback_docs: List of feedback documents
            alpha: Optional fixed weight for content (if None, uses adaptive)
            
        Returns:
            tuple: (final_scores, alpha_used, content_scores, collab_scores)
        """
        if not self.is_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        # Compute content-based scores
        content_scores = self.compute_content_similarity(user_query)
        
        # Compute collaborative filtering scores
        collab_scores = self.compute_collaborative_scores(course_codes, feedback_docs)
        
        # Determine alpha (content weight)
        if alpha is None:
            alpha = self.adaptive_alpha(len(feedback_docs))
        
        # Normalize scores to 0-1 range for fair combination
        content_scores_norm = content_scores  # Already 0-1 from cosine similarity
        
        # Combine scores
        final_scores = alpha * content_scores_norm + (1 - alpha) * collab_scores
        
        return final_scores, alpha, content_scores, collab_scores
    
    def get_top_recommendations(self, final_scores, course_codes, top_k=10):
        """
        Get top K course recommendations based on scores
        
        Args:
            final_scores: Array of recommendation scores
            course_codes: List of course codes
            top_k: Number of recommendations to return
            
        Returns:
            List of tuples: [(course_code, score), ...]
        """
        # Get indices of top scores
        top_indices = np.argsort(final_scores)[::-1][:top_k]
        
        # Create list of (course_code, score) tuples
        recommendations = [
            (course_codes[idx], float(final_scores[idx]))
            for idx in top_indices
        ]
        
        return recommendations
    
    # =============== EVALUATION FUNCTIONS ===============
    
    def precision_at_k(self, recommended_ids, relevant_ids, k):
        """
        Calculate Precision@K metric
        
        Args:
            recommended_ids: List of recommended course codes
            relevant_ids: List of relevant course codes (ground truth)
            k: Number of top recommendations to consider
            
        Returns:
            Precision@K score (0-1)
        """
        if k == 0 or len(recommended_ids) == 0:
            return 0.0
        
        recommended_k = recommended_ids[:k]
        relevant_set = set(relevant_ids)
        
        hits = sum(1 for course_id in recommended_k if course_id in relevant_set)
        return hits / k
    
    def hit_rate_at_k(self, recommended_ids, relevant_ids, k):
        """
        Calculate Hit Rate@K metric (binary: did we get at least one hit?)
        
        Args:
            recommended_ids: List of recommended course codes
            relevant_ids: List of relevant course codes (ground truth)
            k: Number of top recommendations to consider
            
        Returns:
            1.0 if at least one hit, 0.0 otherwise
        """
        if len(recommended_ids) == 0:
            return 0.0
        
        recommended_k = recommended_ids[:k]
        relevant_set = set(relevant_ids)
        
        for course_id in recommended_k:
            if course_id in relevant_set:
                return 1.0
        
        return 0.0
    
    def recall_at_k(self, recommended_ids, relevant_ids, k):
        """
        Calculate Recall@K metric
        
        Args:
            recommended_ids: List of recommended course codes
            relevant_ids: List of relevant course codes (ground truth)
            k: Number of top recommendations to consider
            
        Returns:
            Recall@K score (0-1)
        """
        if len(relevant_ids) == 0:
            return 0.0
        
        recommended_k = recommended_ids[:k]
        relevant_set = set(relevant_ids)
        
        hits = sum(1 for course_id in recommended_k if course_id in relevant_set)
        return hits / len(relevant_ids)
    
    def evaluate_recommendations(self, recommended_ids, relevant_ids, k_values=[3, 5, 10]):
        """
        Evaluate recommendations using multiple metrics
        
        Args:
            recommended_ids: List of recommended course codes
            relevant_ids: List of relevant course codes (ground truth)
            k_values: List of K values to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        results = {}
        
        for k in k_values:
            results[f"precision@{k}"] = self.precision_at_k(recommended_ids, relevant_ids, k)
            results[f"recall@{k}"] = self.recall_at_k(recommended_ids, relevant_ids, k)
            results[f"hit_rate@{k}"] = self.hit_rate_at_k(recommended_ids, relevant_ids, k)
        
        return results


# =============== GLOBAL INSTANCE ===============
# Create a single global instance to be used across the application
recommendation_engine = RecommendationEngine()

# Auto-load models on import (optional, can be called explicitly)
def initialize_engine():
    """Initialize the recommendation engine"""
    success = recommendation_engine.load_models()
    if success:
        print("✅ Recommendation engine initialized successfully")
    else:
        print("⚠️  Recommendation engine initialized but models not loaded")
        print("   Run 'python rebuild_models.py' to build models")
    return success