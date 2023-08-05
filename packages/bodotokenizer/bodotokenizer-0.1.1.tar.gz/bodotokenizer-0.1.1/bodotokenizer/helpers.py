"""
Contains helpers for normalizations
"""

SINGLE_QUOTE = {
    "‘",
    "‛",
    "’",
    "❛", 
    "❜", 
    "`", 
    "´", 
    "‘", 
    "’",
    "ʼ" #print(u'\u02bc') U+02BC
}

DOUBLE_QUOTE = {
    "''",
    "„",
    "“",
    "‟",
    "”",
    "❝",
    "❞",
    "``",
    "´´",
}

DARI_VARIATIONS = {
    "\|", # escape | for re compile
}
