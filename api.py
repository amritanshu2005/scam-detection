"""
Alternative serverless entry point for Vercel
"""
from api.index import handler

__all__ = ['handler']
