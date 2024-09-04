import pymorphy2


def expand(words_collection):
    analyzer = pymorphy2.MorphAnalyzer()
    all_forms = set()
    for word in words_collection:
        predictions = analyzer.parse(word)
        if len(predictions) == 0:
            # TODO: какие-нибудь логи об очень странном слове
            continue
        all_forms = all_forms.union(
            lexeme.word for lexeme in predictions[0].lexeme)
    return all_forms
