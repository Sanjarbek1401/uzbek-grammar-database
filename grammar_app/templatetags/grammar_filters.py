# app/templatetags/grammar_filters.py

from django import template
import re

register = template.Library()

@register.filter
def split_by_line(value):
    """Ma'nolarni qatorlarga ajratish"""
    if value:
        return [line.strip() for line in value.splitlines() if line.strip()]
    return []

@register.filter
def split_examples(value):
    """Misollarni qatorlarga ajratish"""
    if not value or value == "-":
        return []
    
    # <br> bilan ajratilgan misollarni qatorlarga ajratish
    lines = re.split(r'<br>|<br/>', value)
    
    # Raqamlar bilan boshlangan misollarni ajratish
    result = []
    for line in lines:
        line = line.strip()
        if line:
            # Raqam va nuqtani o'chirish (masalan "1. " ni o'chirish)
            cleaned_line = re.sub(r'^\d+\.\s*', '', line)
            result.append(cleaned_line)
    
    return result

@register.filter
def split_lines(value):
    """Split text into lines, removing empty lines"""
    if not value:
        return []
    return [line.strip() for line in value.split('\n') if line.strip()]