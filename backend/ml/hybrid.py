import pandas as pd

feedback = pd.read_csv("ml/data/feedback.csv")

def hybrid_recommend(content_df, user_id):
    user_feedback = feedback[feedback["user_id"] == user_id]
    ratings = user_feedback.groupby("course_code")["rating"].mean().to_dict()

    content_df["rating_score"] = content_df["course_code"].map(ratings).fillna(0)
    content_df["final_score"] = (
        0.7 * content_df["content_score"]
        + 0.3 * (content_df["rating_score"] / 5)
    )

    return content_df.sort_values(by="final_score", ascending=False)
