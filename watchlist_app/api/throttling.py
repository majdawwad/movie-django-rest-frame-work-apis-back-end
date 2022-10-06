from rest_framework import throttling


class ReviewCreateThrottle(throttling.UserRateThrottle):
    scope = 'review-create'


class ReviewListThrottle(throttling.UserRateThrottle):
    scope = 'review-list'
