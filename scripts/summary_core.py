from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import T5Tokenizer, T5ForConditionalGeneration

_textrank = TextRankSummarizer()
_t5_tok = T5Tokenizer.from_pretrained("t5-small")
_t5 = T5ForConditionalGeneration.from_pretrained("t5-small")

def summarize_textrank(text: str, sentence_count: int = 10) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = _textrank(parser.document, sentence_count)
    return " ".join(str(s) for s in summary)

def summarize_t5(text: str) -> str:
    prompt = "Summarize the following legal document in simple English:\n\n" + text[:3000]
    inputs = _t5_tok(prompt, return_tensors="pt", truncation=True)
    outputs = _t5.generate(**inputs, max_length=200, num_beams=4, early_stopping=True)
    return _t5_tok.decode(outputs[0], skip_special_tokens=True)
