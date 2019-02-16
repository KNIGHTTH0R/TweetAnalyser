class LocalGrammarManager():

    def __init__(self, center_word, left_list, right_list, num_left_right=1)):
        """
        Parameters.
        center_word: the base word that we're looking for,
        left_list, right_list: lists of words that can appear to the left/right
        of the center word,
        num_left_right: how many words to the left/right of the center word to consider
        """
        self.center_word = center_word
        self.left_list = left_list
        self.right_list = right_list
        self.num_left_right = num_left_right

    def extract_local_grammar(self, text):
        pass

