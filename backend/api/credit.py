from django.db.models import Avg, Count
from .models import Review


def recalculate_credit_score(user):
    """信用分 = 贝叶斯平滑(默认5.0, 先验2条) + 收到评分的均值，范围约 1.0~5.0"""
    stats = Review.objects.filter(target=user).aggregate(avg=Avg('rating'), count=Count('id'))
    count = stats['count'] or 0
    if count == 0:
        user.credit_score = 5.0
    else:
        prior_mean = 5.0
        prior_count = 2
        avg = float(stats['avg'])
        user.credit_score = round(
            (prior_mean * prior_count + avg * count) / (prior_count + count),
            1,
        )
    user.save(update_fields=['credit_score'])
    return user.credit_score


def credit_level_label(score):
    if score >= 4.5:
        return '优秀'
    if score >= 4.0:
        return '良好'
    if score >= 3.0:
        return '一般'
    return '待提升'
