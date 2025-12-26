from database.mongo import mongo

_cached_courses = None

def get_courses():
    global _cached_courses
    if _cached_courses is None:
        _cached_courses = list(mongo.db.courses.find())
    return _cached_courses