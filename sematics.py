import nltk
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
# Ensure necessary NLTK data is downloaded
for resource in ["stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource)

def semantics_analysis(text: str):
    """
    Performs semantic analysis on the input text.
    Returns:
        - word_counts: dict of word frequencies (excluding stopwords)
        - analysis: dict containing top words, semantic themes, and sentiment
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    word_counts = {}
    words = text.split()

    for word in words:
        word = word.lower()
        if not word.isalpha():
            continue
        if word in stop_words:
            continue
        lemma = lemmatizer.lemmatize(word)
        word_counts[lemma] = word_counts.get(lemma, 0) + 1

    # Prepare analysis summary
    analysis = {
        "top_words": sorted(word_counts.items(), key=lambda x: x[1], reverse=True),
        "themes": {},
        "sentiment": {"polarity": 0.0, "subjectivity": 0.0}
    }

    # Semantic themes based on WordNet lexical categories
    for word, freq in analysis["top_words"]:
        synsets = wn.synsets(word)
        if synsets:
            # Choose most frequent synset as best guess
            synset = max(synsets, key=lambda s: s.lemmas()[0].count() if s.lemmas() else 0)
            topic = synset.lexname()
            analysis["themes"][topic] = analysis["themes"].get(topic, 0) + freq

    # Sentiment analysis on the full original sentence
    blob = TextBlob(text)
    analysis["sentiment"]["polarity"] = round(blob.sentiment.polarity, 2)
    analysis["sentiment"]["subjectivity"] = round(blob.sentiment.subjectivity, 2)

    return word_counts, analysis