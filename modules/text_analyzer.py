from textblob import TextBlob

def analyze_text(text):
    blob = TextBlob(text)

    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    return {
        "Sentiment Score": sentiment,
        "Subjectivity": subjectivity
    }