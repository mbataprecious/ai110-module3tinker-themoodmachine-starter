"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    # Standard positive words
    "happy",
    "great",
    "good",
    "love",
    "like",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "joy",
    "glad",
    "beautiful",
    "wonderful",
    "excellent",
    "perfect",
    "best",
    # Slang for "good/awesome"
    "fire",        # "that song is fire"
    "lit",         # "the party was lit"
    "dope",        # "that's so dope"
    "sick",        # "sick moves!"
    "tight",       # "that's tight"
    "fresh",       # "fresh kicks"
    "bomb",        # "this pizza is bomb"
    "wicked",      # "wicked cool" (regional slang)
    "slaps",       # "this song slaps"
    "hits",        # "this hits different"
    "iconic",      # "that's iconic"
    "goat",        # "he's the goat" (greatest of all time)
    "vibes",       # "good vibes"
    "clean",       # "that car is clean"
    "solid",       # "solid choice"
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "dislike",
    "annoyed",
    "frustrated",
    "disappointed",
    "hurt",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey stressed about the exam but no cap I think I aced it 😅",
    "I absolutely love waking up at 5am for work 🙃",
    "Just got ghosted lmao... anyway pizza time 🍕",
    "Feeling kinda empty ngl but the sunset hit different today 🌅",
    "My boss said 'great job' in the most dead voice possible 💀",
    "your presentation was fire",
    "he's the goat",
    "I can't believe I have to work on a Saturday",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "Lowkey stressed about the exam but no cap I think I aced it 😅"
    "negative",  # "I absolutely love waking up at 5am for work 🙃" (sarcasm)
    "mixed",     # "Just got ghosted lmao... anyway pizza time 🍕"
    "mixed",     # "Feeling kinda empty ngl but the sunset hit different today 🌅"
    "neutral",   # "My boss said 'great job' in the most dead voice possible 💀",
    "positive",  # "your presentation was fire",
    "positive",  # "he's the goat",
    "negative",  # "I can't believe I have to work on a Saturday"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
