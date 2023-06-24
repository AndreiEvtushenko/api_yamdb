def get_rating(self, obj):
    ratings = obj.reviews_title_id.all()
    scores = [rating.score for rating in ratings]

    if scores:
        return round(sum(scores) / len(scores))
    return None
