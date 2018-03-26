USE_MECAB_BINIDING = True
try:
    import MeCab
    _model = MeCab.Model("-Owakati")
    _lattice = _model.createLattice()
except ImportError:
    USE_MECAB_BINIDING = False


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