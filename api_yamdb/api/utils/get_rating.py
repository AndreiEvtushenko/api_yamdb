def get_rating(obj):
    ratings = obj.reviews_title_id.all()
    scores = [rating.score for rating in ratings]

    if scores:
        return round(sum(scores) / len(scores))
    return None
