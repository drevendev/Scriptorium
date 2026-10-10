"""Reader labels for the versioned metric IDs; no metric calculations."""
from typing import Final

METRIC_LABELS: Final = {
    "fantlab.general.characters": "Characters",
    "fantlab.general.words": "Words",
    "scriptorium.general.sentences": "Sentences (Scriptorium)",
    "fantlab.general.mean_word_length_chars": "Mean word length",
    "fantlab.general.mean_sentence_length_chars": "Mean sentence length",
    "fantlab.dialogue.mean_narration_sentence_length_chars": "Mean narration sentence length",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars": "Mean dialogue sentence length",
    "fantlab.dialogue.share_percent": "Dialogue character share",
    "fantlab.dialogue.author_text_inside_dialogue_percent": "Author remarks within dialogue",
    "fantlab.vocabulary.unique_words": "Distinct surface words",
    "fantlab.vocabulary.active_dictionary": "Distinct dictionary words",
    "fantlab.vocabulary.active_nondictionary": "Distinct out-of-dictionary words",
    "fantlab.vocabulary.uasz_3000": "Dictionary variety · 3,000-word window",
    "fantlab.vocabulary.uasz_10000": "Dictionary variety · 10,000-word window",
    "fantlab.vocabulary.uasz_100000": "Dictionary variety · 100,000-word window",
    **{f"fantlab.punctuation.{metric}.per_1000_words": f"{label} per 1,000 words"
       for metric, label in {
           "comma": "Commas", "period": "Periods", "dash": "Dashes",
           "exclamation": "Exclamation marks", "question": "Question marks",
           "ellipsis": "Ellipses", "exclamation_ellipsis": "Exclamation–ellipsis sequences",
           "question_ellipsis": "Question–ellipsis sequences",
           "triple_exclamation": "Triple-exclamation sequences",
           "question_exclamation": "Question–exclamation sequences",
           "quote": "Quotation marks", "parentheses": "Opening parentheses",
           "colon": "Colons", "semicolon": "Semicolons",
       }.items()},
}
