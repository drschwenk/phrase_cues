import spacy
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import sent_tokenize


nlp = spacy.load('en')
core_nlp_base = '/Users/schwenk/wrk/animation_gan/phrase_cues/deps/stanford_core_nlp/stanford-corenlp-full-2017-06-09/'

parser = StanfordParser(path_to_jar=core_nlp_base + 'stanford-corenlp-3.8.0.jar',
                        path_to_models_jar=core_nlp_base +'stanford-corenlp-3.8.0-models.jar')


def const_parse(doc):
    sentences = sent_tokenize(doc)
    sent_parses = [list(i)[0] for i in parser.raw_parse_sents(sentences)]
    return sent_parses


def build_simple_parse_tree(nltk_tree):

    return


def coref(doc):
    pass


def parse_description(vid_text):
    doc = nlp(vid_text)
    # pos_tags = [(word.text, word.pos_) for word in doc]
    noun_phrase_chunks = [np.text for np in doc.noun_chunks]
    constituent_parse = const_parse(vid_text)
    pos_tags = [sent.pos() for sent in constituent_parse]
    parses = {
                'noun_phrase_chunks': noun_phrase_chunks,
                'pos_tags': pos_tags,
                'constituent_parse': constituent_parse
             }

    return parses


class Tree(object):
    def __init__(self, nltk_parented_tree):
        self.subtrees = []
        self._node_lookup = {}
        self.leaves = []
        for node in list(nltk_parented_tree.subtrees()):
            nkey = str(node.treeposition())
            if len(node.leaves()) > 1 or len(list(node.subtrees())) > 1:
                self.subtrees.append(Node(node))
            else:
                node.set_label(' '.join([node.label(), node.leaves()[0]]))
                leaf_node = Node(node)
                self.subtrees.append(leaf_node)
                self.leaves.append(leaf_node)
            self._node_lookup[nkey] = self.subtrees[-1]

        self.root_node = [node for node in self.subtrees if node.value == 'ROOT'][0]
        self.word_pos_to_node = {idx: node for idx, node in enumerate(self.leaves)}

        for node in self.subtrees:
            node.left_sibling = self._node_lookup.get(node.left_sibling)
            node.right_sibling = self._node_lookup.get(node.right_sibling)
            node.parent = self._node_lookup.get(node.parent)


class Node(object):
    def __init__(self, nltk_node):
        self.value = nltk_node.label()  # (tag,word/phrase)
        self.left_sibling = Node.get_tree_position(nltk_node)  # Instance of class Node
        self.right_sibling = Node.get_tree_position(nltk_node)  # Instance of class Node
        self.parent = Node.get_tree_position(nltk_node.parent())  # Instance of class Node

    @classmethod
    def get_tree_position(cls, node):
        if node:
            return str(node.treeposition())
        else:
            return
