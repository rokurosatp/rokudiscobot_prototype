import logging
import shutil
import subprocess

USE_MECAB_BINIDING = True
try:
    import MeCab
    _model = MeCab.Model("-Owakati")
    _lattice = _model.createLattice()
except ImportError:
    logging.warning("no python module named MeCab. If you would like to use mecab binding, type this command")
    logging.warning("\tapt install mecab, libmecab-dev,mecab-ipadic-utf8")
    logging.warning("\tpip install mecab-python3")
    USE_MECAB_BINIDING = False

if USE_MECAB_BINIDING:
    def in_class_of(sentence, classes={}):
        tagger = _model.createTagger()
        _lattice.set_sentence(sentence)
        tagger.parse(_lattice)
        words = _lattice.toString().split()
        for word in words:
            if word in classes:
                return True
        return False

    def tokenize_mecab(sentence):
        model = MeCab.Model()
        lattice = model.createLattice()
        tagger = model.createTagger()
        lattice.set_sentence(sentence)
        tagger.parse(lattice)
        return lattice.toString().rstrip("\n\r")
elif shutil.which("mecab"):
    def in_class_of(sentence, classes={}):
        results = subprocess.run("mecab -Owakati", sentence.encode("utf8"), stdout=subprocess.PIPE)
        words = results.stdout.decode("utf8").rstrip("\r\n").split()
        for word in words:
            if word in classes:
                return True
        return False

    def tokenize_mecab(sentence):
        results = subprocess.run("mecab", sentence.encode("utf8"), stdout=subprocess.PIPE)
        return results.stdout.decode("utf8").rstrip("\n\r")
else:
    def in_class_of(sentence, classes=False):
        return False
    
    def tokenize_mecab(sentence):
        return "Not installed Mecab!"