"""
blocklist.py

This file contains the blocklist of the JWT tokens. It will be imported by app
and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""
from redis import Redis


jwt_redis_blocklist = Redis(
    host="redis", port=6379, db=0, decode_responses=True
)
