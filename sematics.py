import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from textblob import TextBlob

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
def semantics_analysis(self,row: str):
    """
    Gets analisys for word user uses
    """
    spliter = row.split()
    results=dict()
    stop_words = set(stopwords.words("english"))
    for i in spliter:
        i = i.lower()
        if not i.isalpha():
            continue
        if i in stop_words:
            continue
        results[i] = results.get(i, 0) + 1
    analysis = {
        "top_words": [],
        "themes": {},
        "sentiment": {"polarity": 0, "subjectivity": 0}
        }
    analysis["top_words"] = sorted(results.items(), key=lambda x: x[1], reverse=True)

    for word, freq in analysis["top_words"]:
        synsets = wn.synsets(word)
        if synsets:
            topic = synsets[0].lexname()
            if topic not in analysis["themes"]:
                analysis["themes"][topic] = 0
            analysis["themes"][topic] += freq

    sentence = ' '.join([word for word in results])
    blob = TextBlob(sentence)
    analysis["sentiment"]["polarity"] = round(blob.sentiment.polarity,2)
    analysis["sentiment"]["subjectivity"] = round(blob.sentiment.subjectivity,2)
    return results,analysis
