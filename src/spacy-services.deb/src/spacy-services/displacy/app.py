# coding: utf8
from __future__ import unicode_literals
import threading

import hug
from hug_middleware_cors import CORSMiddleware
import spacy

MODELS = {}

lock = threading.Lock()


def load_model_once(model):

    if not model in MODELS:
        lock.acquire()
        try:
            if not model in MODELS:
                        print("Loading model {}".format(model))
                        MODELS[model] = spacy.load(model)
                        print("Loaded model {}".format(model))
            lock.release()
        except:
            lock.release()
            raise

    return MODELS[model]


def get_model_desc(nlp, model_name):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@hug.get("/models")
def models():
    return {
        "models": {name: get_model_desc(nlp, name) for name, nlp in MODELS.items()},
        "labels": {name: nlp.pipe_labels for name, nlp in MODELS.items()},
    }


@hug.post("/dep")
def dep(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get dependencies for displaCy visualizer."""
    nlp = load_model_once(model)
    doc = nlp(text)
    options = {
        "collapse_punct": collapse_punctuation,
        "collapse_phrases": collapse_phrases,
    }
    return spacy.displacy.parse_deps(doc, options)


@hug.post("/ent")
def ent(text: str, model: str):
    """Get entities for displaCy ENT visualizer."""
    nlp = load_model_once(model)
    doc = nlp(text)
    return [
        {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
        for ent in doc.ents
    ]


@hug.post('/sents')
def sents(text: str, model: str):
    """Get sentences from text by sentence segmentation."""
    nlp = load_model_once(model)
    doc = nlp(text)

    return [sent.text
            for sent in doc.sents]


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8080)
