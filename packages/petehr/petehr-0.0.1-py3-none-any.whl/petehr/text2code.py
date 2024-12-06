import csv
import re


class Tnode:
    def __init__(self):
        self.children = {}  # TrieNode
        self.code = None


class Text2Code:
    def __init__(self, dictionary_path=None):
        """
        Initialize the Text2Cui processor and optionally load a dictionary.
        """
        self.root = Tnode()
        # Flag to check if the dictionary is loaded
        self.dictionary_loaded = False

        if dictionary_path:
            self.load_dictionary(dictionary_path)

    def add_mapping(self, text, code):
        """
        Add text from dictionary into the Trie and its associated code.
        """
        text_words = text.split(" ")

        cur = self.root
        for word in text_words:
            if word not in cur.children:
                cur.children[word] = Tnode()
            cur = cur.children[word]
        cur.code = code

    def load_dictionary(self, file_path):
        """
        Load mappings from a CSV file into the Trie.
        """
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                self.add_mapping(row[0].lower(), row[1])
        self.dictionary_loaded = True
        print(f"Dictionary loaded sucessfully from {file_path}")

    def convert(self, inp_txt):
        """
        Traverse the input text to identify concepts that can be mapped to CUIs
        Parameters:
        - inp_txt: The text to process.

        Returns:
        - List of identified CUIs.
        """
        if not self.dictionary_loaded:
            raise ValueError(
                "Dictionary not loaded! Please load the dictionary using load_dictionary function"
            )

        # Normalize and tokenize the input text
        inp_txt = re.sub(r"[\r\n]+|[^\w\s']", " ", inp_txt.lower())
        inp_txt_words = inp_txt.split(" ")

        # Traverse the Trie to identify CUIs
        codes_ided = []
        cur = self.root
        last = ""

        inp_txt_len = len(inp_txt_words)
        i = 0
        j = 1

        while i < inp_txt_len:
            if inp_txt_words[i] not in cur.children:
                if last:  # Append the last matched code
                    codes_ided.append(last)
                cur = self.root
                last = ""
                if j:
                    j = 0
                    continue
            else:
                cur = cur.children[inp_txt_words[i]]
                last = cur.code
            i += 1
            j = 1

        if last:
            codes_ided.append(last)

        return ",".join(codes_ided)
