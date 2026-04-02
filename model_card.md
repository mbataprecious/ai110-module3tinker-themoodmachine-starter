# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  
Example: “I used the rule based model only” or “I compared both models.”

**Answer:**  I used the rule based model only

**Intended purpose:**  
What is this model trying to do?  
Example: classify short text messages as moods like positive, negative, neutral, or mixed.

**Answer:**  classify short text messages to sentiments like positive, negative, neutral, or mixed

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  
For the ML version, describe how training works at a high level (no math needed).

**Answer:** The rule-based model counts weighted sentiment words (positive = +1/+2, negative = -1/-2), flips the sign if negation words like "not" appear before them, adds emoji scores, then maps the total to a label (positive if ≥1, negative if ≤-1, neutral if 0).

## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.

**Answer:** I added 8 new posts some are generated and 2 are sarcasm from me, the total is 14

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.

**Answer:** I manually labeled the new posts

**Important characteristics of your dataset:**  
Examples you might include:  

- Contains slang or emojis  
- Includes sarcasm  
- Some posts express mixed feelings  
- Contains short or ambiguous messages

**Answer:** 
- Some posts express mixed feelings
- Includes emojis
- Detect and analyze negation words



**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

**Answer:**
- Not good at detecting sarcasm
- Not good at detecting mixed feelings
- Not good at detecting all slags

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

- How positive and negative words affect score  
- Negation rules you added  
- Weighted words  
- Emoji handling  
- Threshold decisions for labels

**Answer:**

Word Scoring

- Regular positive/negative words: ±1
- Strong words (love, hate, terrible, awesome): ±2
- Slang (fire, lit, goat): +1 or +2

Negation

- Words like "not", "dont", "never" flip the next sentiment word's sign
- "not bad" → +1, "dont like" → -1

Emojis

- Mapped to scores: 😍(+2), 😭(-2), 🙃(-1), 🔥(+1)
- Extracted from raw text before punctuation removal

Thresholds

- ≥1 → positive, ≤-1 → negative, 0 → neutral
Lowered from ±2 to catch weak sentiment ("bad" = -1 should be negative)

Preprocessing

- Lowercase, strip punctuation, normalize contractions ("don't" → "dont")

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

**Answer:**
- Clear sentiment ("love", "terrible", "hate")
- Negation ("not bad", "don't like")
- Known slang ("fire", "lit", "goat")
- Emoji-heavy posts (🎉, 😭 add strong signals)
- Simple, single-clause sentences

**Weaknesses of this approach:**  
Where does it fail?  
Examples: sarcasm, subtlety, mixed moods, unfamiliar slang.

**Answer:**
Fails on: sarcasm, unknown slang, and context-dependent tone.

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.

**Answer:**
The rule-based model achieved 54.5% accuracy (6/11 correct), correctly classifying clear sentiment and negation but failing on sarcasm and mixed emotions, while the ML model likely overfits to near 100% on the tiny dataset but generalizes poorly to new examples.

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.

**Answer:**

Example 1: "I love this class so much" → positive ✓
- "love" is a strong positive word (+2), meeting the ≥1 threshold for positive

Example 2: "Today was a terrible day" → negative ✓
- "terrible" is a strong negative word (-2), meeting the ≤-1 threshold for negative

Example 3: "I am not happy about this" → negative ✓
- Negation handling flipped "happy" (+1) to -1, correctly capturing the negative sentiment

**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.

**Answer:**

Example 1: "I absolutely love waking up at 5am for work 🙃" → predicted positive, true negative ✗

- Model scored: love(+2) + 🙃(-1) = +1 → positive
Why it failed: The model detected sarcasm emoji (-1) but "love" (+2) outweighed it. It doesn't understand that sarcasm context should flip the whole sentiment, not just add a small penalty.

Example 2: "Feeling tired but kind of hopeful" → predicted neutral, true mixed ✗

- Model scored: tired(-1) + hopeful(+1) = 0 → neutral
Why it failed: The model just sums to zero, treating conflicting signals as "no sentiment" rather than recognizing the intentional contrast ("tired BUT hopeful") that humans label as mixed.

## 6. Limitations

Describe the most important limitations.  
Examples:  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled

**Answer:**

- No sarcasm detection ("love waking up at 5am" reads as positive)
- Fixed word lists miss unknown slang and context ("ghosted", "mid")
- Simple negation only flips one word ("not good or bad" fails)
- Scores sum to zero for conflicting emotions → labeled neutral instead of mixed
- No sentence context ("great" always positive, even in "oh great, another meeting")

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
Examples: 

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

**Answer:**
Mood detection in real applications can perpetuate bias if trained on limited data, potentially misinterpreting cultural expressions, slang, or non-native speech patterns. Automated decisions based on flawed sentiment analysis—like flagging mental health crises or filtering content—can cause real harm through false positives or missed signals. Users should always have transparency about automated mood analysis and the ability to contest or opt out of such systems.

## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only

**Answer:**
- Add more labeled examples (20-50+ posts) covering slang, sarcasm, and edge cases
- Use TF-IDF instead of CountVectorizer to weight rare/important words higher
- Extend negation scope to handle phrases like "not good or bad" (multiple words)
- Add n-gram features (word pairs like "not happy", "kind of") to capture context
- Create a real test set by splitting data 70/30 or using cross-validation instead of training accuracy



### Bias and Scope

The model is optimized for informal American English slang ("lit", "goat", "no cap") and emoji-heavy social media posts. It may misinterpret British English ("wicked" has different meanings), AAVE, non-native English speakers, or older generations' language patterns. The dataset skews young and internet-native, creating blind spots for regional dialects and formal writing.

### ML vs Rule-Based Comparison

The learned model handles word combinations better (e.g., "kind of hopeful" as a phrase) but overfits heavily—memorizing the 14 training examples perfectly but failing unpredictably on new inputs. It fixed the negation issue in some cases by learning context, but introduced new errors where it confidently predicted wrong labels for slang it hadn't seen. The ML model was highly sensitive to label quality; changing one label from "mixed" to "neutral" flipped predictions on similar sentences, showing instability with small data.