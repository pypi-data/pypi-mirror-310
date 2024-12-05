import csv
import re


class Tnode:
    def __init__(self):
        self.children = {}  # TrieNode
        self.cui = None


class Text2Cui:
    def __init__(self, dictionary_path=None):
        """
        Initialize the Text2Cui processor and optionally load a dictionary.
        """
        self.root = Tnode()
        # Flag to check if the dictionary is loaded
        self.dictionary_loaded = False

        if dictionary_path:
            self.load_mappings(dictionary_path)

    def add_mapping(self, text, cui):
        """
        Add text from dictionary into the Trie and its associated CUI.
        """
        text_words = text.split(" ")

        cur = self.root
        for word in text_words:
            if word not in cur.children:
                cur.children[word] = Tnode()
            cur = cur.children[word]
        cur.cui = cui

    def load_mappings(self, file_path):
        """
        Load mappings from a CSV file into the Trie.
        """
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                self.add_mapping(row[0], row[1])
        self.dictionary_loaded = True
        print(f"Dictionary loaded from {file_path}")

    def traverse(self, inp_txt):
        """
        Traverse the input text to identify concepts that can be mapped to CUIs
        Parameters:
        - inp_txt: The text to process.

        Returns:
        - List of identified CUIs.
        """
        if not self.dictionary_loaded:
            raise ValueError(
                "Dictionary not loaded. Please load a dictionary using load_mappings function"
            )

        # Normalize and tokenize the input text
        inp_txt = re.sub(r"[\r\n]+|[^\w\s']", " ", inp_txt.lower())
        inp_txt_words = inp_txt.split(" ")

        # Traverse the Trie to identify CUIs
        cuis_ided = []
        cur = self.root
        last = ""

        inp_txt_len = len(inp_txt_words)
        i = 0
        j = 1

        while i < inp_txt_len:
            if inp_txt_words[i] not in cur.children:
                if last:  # Append the last matched CUI
                    cuis_ided.append(last)
                cur = self.root
                last = ""
                if j:
                    j = 0
                    continue
            else:
                cur = cur.children[inp_txt_words[i]]
                last = cur.cui
            i += 1
            j = 1

        if last:
            cuis_ided.append(last)

        return ",".join(cuis_ided)
