from rest_framework.throttling import ScopedRateThrottle


class CustomMovieThrottle(ScopedRateThrottle):
    scope = "movie"
