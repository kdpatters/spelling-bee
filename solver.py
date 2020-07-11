import json
import numpy as np
import pickle

MIN_LENGTH = 4
TREE_FILE = "tree.pickle"
WORDS_FILE = "twl06_us_scrabble.txt"
NEXT = 100

# Prefix tree with keys of sorted, unique letters for
# values of the full, unsorted words.
class Node:
    def __init__(self, root=0):
        self.words = []
        self.children = {}
        self.root = root
    def add_child(self, char):
        # Add a child to the current node
        if not (char in self.children):
            self.children[char] = Node()
        return self.children[char]
    def match_child(self, char):
        # Return child node or none if no matching child found
        if char in self.children:
            return self.children[char]
        else:
            return None
    def match_or_add(self, char):
        # Return matching child or create one if it does not exist
        child = self.match_child(char)
        if not child:
            child = self.add_child(char)
        return child
    def add_word_to_node(self, word):
        self.words.append(word)
    def add_word_to_tree(self, word):
        # Add a word to the tree using provided
        # This should only be done from root node to avoid issues
        assert(self.root)
        current = self
        word = word.strip()
        for char in self.sorted_unique_char(word):
            current = current.match_or_add(char)
        current.add_word_to_node(word)
    def sorted_unique_char(self, word):
        # Get all unique chars
        unique = list(set(word.strip().lower()))
        # Check that all characters are valid
        #for char in unique:
        #    if not (char in string.ascii_lowercase):
        #        print("Found invalid character when building tree: %s" % char)
        #    assert(char in string.ascii_lowercase)
        # Sort characters
        sorted = np.sort(unique)
        return sorted
    def return_words(self):
        return self.words
    def search_words(self, letters):
        assert(self.root)
        letters = self.sorted_unique_char(letters)
        found_words = self.search_helper(self, letters)
        return found_words
    def search_helper(self, subtree, suffix):
        # Searches subtree for the given suffix and returns matching words
        found_words = []
        for i, char in enumerate(suffix):
            # Check if any words containing the current character 'char' exist...
            new = subtree.match_child(char)
            # Found some matches!
            if new:
                found_words += new.return_words()
                found_words += self.search_helper(new, suffix[i+1:])
        return found_words

def get_words(tree, letters, magic_letter):
    print("Query: \"%s\" with magic letter \'%s\'" % (letters, magic_letter))
    print("Searching tree for matching words using these letters")
    # Search letters must include the "magic letter"
    assert(magic_letter in letters)
    found_words = tree.search_words(letters)
    def predicate(w): (len(w) >= MIN_LENGTH) and (magic_letter in w)
    valid = list(filter(predicate, found_words))
    return valid

def load_words(dict_file):
    print("Loading dictionary from file %s" % dict_file)
    with open(dict_file, "r") as fp:
        if dict_file.endswith(".json"):
            words_dict = json.load(fp)
        else:
            words_dict = fp.readlines()
    return words_dict

def make_tree(words_dict):
    print("Generating prefix tree")
    # Create root node of tree
    root = Node(root=1)
    for word in words_dict:
        # Add sorted unique string to tree
        root.add_word_to_tree(word)
    return root

if __name__ == '__main__':
    try:
        print("Looking for pre-generated tree to unpickle")
        with open(TREE_FILE, 'rb') as fp:
            tree = pickle.load(fp)
        print("Loaded tree from pickle successfully")
    except:
        english_words = load_words(WORDS_FILE)
        tree = make_tree(english_words)
        with open(TREE_FILE, 'wb') as fp:
            pickle.dump(tree, fp)

    while(True):
        letters = input("Enter letters: ")
        mag = input("Enter golden letter: ")
        words = get_words(tree, letters, mag)
        print("%d total words found" % len(words))
        for i, word in enumerate(np.sort(words)):
            print("%d: %s" % (i, word))
            if (i > 0) & ((i % NEXT) == 0):
                input("Press any key to display the next %d words" % NEXT)