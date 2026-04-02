# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""
import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A rule based mood classifier with emoji support and weighted word scoring.
    """

    # Emojis and their sentiment weights (positive = +1, negative = -1)
    EMOJI_SENTIMENTS: Dict[str, int] = {
        # Positive emojis
        '😀': 1, '😃': 1, '😄': 1, '😁': 1, '😊': 1, '🙂': 1,
        '😍': 2, '🥰': 2, '😘': 1, '😗': 1, '☺️': 1,
        '🤩': 2, '🥳': 2, '😎': 1, '👍': 1, '💪': 1,
        '❤️': 2, '💖': 2, '💕': 1, '💯': 1, '🔥': 1,
        '🎉': 2, '✨': 1, '🙌': 1, '😂': 1, '🤣': 1,
        '😋': 1, '🤗': 1, '🌟': 1, '🌈': 1, '🍕': 1,
        # Negative emojis
        '😢': -1, '😭': -2, '😞': -1, '😔': -1, '😟': -1,
        '😕': -1, '🙁': -1, '☹️': -1, '😣': -1, '😫': -1,
        '😩': -2, '😤': -1, '😠': -2, '😡': -2, '🤬': -2,
        '💔': -2, '😰': -1, '😥': -1, '😓': -1, '😒': -1,
        '🙄': -1, '😬': -1, '🤢': -1, '🤮': -1, '🥴': -1,
        # Sarcasm/ambiguous emojis (count as slightly negative or neutral)
        '🙃': -1,  # upside down smiley (often sarcastic)
        '😑': 0,   # expressionless
        '😐': 0,   # neutral
        '😶': 0,   # no mouth
        '💀': -1,  # skull (often used for "dead"/awkward situations)
    }

    # Text emoticons
    TEXT_EMOTICONS: Dict[str, int] = {
        ':)': 1, ':-)': 1, ':]': 1, ':-]': 1,
        ':(': -1, ':-(': -1, ':[': -1, ':-[': -1,
        ';)': 1, ';-)': 1,
        ':D': 2, ':-D': 2,
        ':p': 1, ':-p': 1, ':P': 1, ':-P': 1,
        ':/': -1, ':-/': -1, ':\\': -1, ':-\\': -1,
        ':|': 0, ':-|': 0,
        ':\'(': -2, ':\'-("': -2,
        '<3': 1, '</3': -1,
    }

    # Negation words that flip or dampen sentiment
    NEGATION_WORDS: set = {
        'not', 'no', 'never', 'neither', 'nobody', 'nothing', 'nowhere',
        'dont', 'doesnt', 'didnt', 'wont', 'wouldnt', 'cant', 'cannot',
        'couldnt', 'shouldnt', 'isnt', 'arent', 'wasnt', 'werent', 'hasnt',
        'havent', 'hadnt', 'mustnt', 'aint',
    }

    # Strong words have higher weights
    STRONG_POSITIVE_WORDS: Dict[str, int] = {
        'love': 2,
        'amazing': 2,
        'awesome': 2,
        'excellent': 2,
        'perfect': 2,
        'wonderful': 2,
        'best': 2,
        # Slang (often used as strong compliments)
        'fire': 2,      # "your presentation was fire"
        'hot': 2,       # "you look hot"
        'lit': 2,       # "the party was lit"
        'dope': 2,      # "that's so dope"
        'sick': 2,      # "sick moves!"
        'goat': 2,      # "he's the goat"
    }

    STRONG_NEGATIVE_WORDS: Dict[str, int] = {
        'hate': -2,
        'terrible': -2,
        'awful': -2,
        'horrible': -2,
        'disgusting': -2,
        'worst': -2,
    }

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements made:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Removes punctuation (keeps only alphanumeric characters and spaces)
          - Normalizes contractions (don't -> dont, won't -> wont)
          - Splits on whitespace to create tokens

        Future ideas:
          - Normalize repeated characters ("soooo" -> "soo")
        """
        # Lowercase and strip whitespace
        cleaned = text.strip().lower()

        # Remove punctuation: keep only letters, numbers, and spaces
        # Keep apostrophes temporarily for contraction handling
        cleaned = re.sub(r'[^a-z0-9\s\']', '', cleaned)

        # Normalize contractions by removing apostrophes
        # This converts "don't" -> "dont", "won't" -> "wont", etc.
        cleaned = cleaned.replace("'", "")

        # Split on whitespace to get tokens
        tokens = cleaned.split()

        # Print tokens for debugging/verification
        print(f"  Tokens: {tokens}")

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _extract_emojis(self, text: str) -> List[str]:
        """Extract all emoji characters from text."""
        return [char for char in text if char in self.EMOJI_SENTIMENTS]

    def _extract_text_emoticons(self, text: str) -> List[str]:
        """Extract text-based emoticons from text."""
        found = []
        for emoticon in sorted(self.TEXT_EMOTICONS.keys(), key=len, reverse=True):
            if emoticon in text:
                found.append(emoticon)
                # Remove to avoid double-counting overlapping patterns
                text = text.replace(emoticon, '')
        return found

    def _get_word_weight(self, token: str) -> int:
        """Get the sentiment weight for a word (0 if not a sentiment word)."""
        if token in self.STRONG_POSITIVE_WORDS:
            return self.STRONG_POSITIVE_WORDS[token]
        elif token in self.STRONG_NEGATIVE_WORDS:
            return self.STRONG_NEGATIVE_WORDS[token]
        elif token in self.positive_words:
            return 1
        elif token in self.negative_words:
            return -1
        return 0

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Improvements:
          - Words have weighted scores (strong positive/negative words count more)
          - Negation handling: "not happy" flips sentiment, "dont like" = negative
          - Emojis contribute to sentiment (positive emojis +1, negative -1, strong ones ±2)
          - Text emoticons like :) and :( are also scored
        """
        score = 0
        emoji_hits: List[str] = []
        emoticon_hits: List[str] = []
        word_hits: List[Tuple[str, int]] = []  # (word, weight)

        # 1. Get tokens from preprocess
        tokens = self.preprocess(text)

        # 2. Score words with weights and negation handling
        negation_active = False
        for i, token in enumerate(tokens):
            # Check if this is a negation word
            if token in self.NEGATION_WORDS:
                negation_active = True
                continue

            weight = self._get_word_weight(token)

            if weight != 0:
                # Apply negation: flip the sign of the weight
                if negation_active:
                    original_weight = weight
                    weight = -weight
                    word_hits.append((f"NOT_{token}" if weight < 0 else token, weight))
                    negation_active = False  # Negation applies to one word only
                else:
                    word_hits.append((token, weight))

                score += weight

        # 3. Extract and score emojis from original text
        emojis = self._extract_emojis(text)
        for emoji in emojis:
            emoji_score = self.EMOJI_SENTIMENTS.get(emoji, 0)
            score += emoji_score
            if emoji_score != 0:
                emoji_hits.append(f"{emoji}({emoji_score:+d})")

        # 4. Extract and score text emoticons
        emoticons = self._extract_text_emoticons(text)
        for emoticon in emoticons:
            emoticon_score = self.TEXT_EMOTICONS.get(emoticon, 0)
            score += emoticon_score
            if emoticon_score != 0:
                emoticon_hits.append(f"{emoticon}({emoticon_score:+d})")

        # Debug output
        print(f"    Words: {word_hits}")
        print(f"    Emojis: {emoji_hits}")
        print(f"    Emoticons: {emoticon_hits}")
        print(f"    Total Score: {score}")

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Threshold mapping:
          - score >= 1   -> "positive"
          - score <= -1  -> "negative"
          - score == 0   -> "neutral" or "mixed"

        Note: Previously used stricter thresholds (>=2, <=-2) but that was
        too conservative for single-word sentiment ("bad" = -1 should be negative).
        """
        score = self.score_text(text)

        if score >= 1:
            return "positive"
        elif score <= -1:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
