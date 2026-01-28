from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def explain_textrank(text: str, sentence_count: int = 10):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    document = parser.document
    summarizer = TextRankSummarizer()

    summary = summarizer(document, sentence_count)
    sentences = list(document.sentences)
    total = len(sentences)

    explanation = []

    for rank, s in enumerate(summary, 1):
        pos = sentences.index(s)
        if pos < total * 0.3:
            section = "Facts / Background"
        elif pos < total * 0.7:
            section = "Legal Reasoning"
        else:
            section = "Judgment / Decision"

        explanation.append({
            "rank": rank,
            "sentence": str(s),
            "section": section
        })

    return explanation
