"""Cache-related exceptions"""

from .base import PepperPyError


class CacheError(PepperPyError):
    """Base cache error"""


class CacheConnectionError(CacheError):
    """Cache connection error"""


class CacheKeyError(CacheError):
    """Cache key error"""


class CacheValueError(CacheError):
    """Cache value error""" 