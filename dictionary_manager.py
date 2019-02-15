class DictionaryManager():

    # TO-DO: Create method which generates variants of terms.
    # eg. if 'snow' is a term, Twitter variant might be '#snow'
    # Make each dictionary an object?

    def phrases_from_files(filenames):
        """
        This method takes a list of file names and returns a list
        of unique phrases in those files.
        """

        if not filenames or type(filenames) is not list:
            print("DictionaryManager.phrases_from_files() Error :: argument 'filenames' must be a list.")
            return None

        phrases = set()
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = f.readlines()[1:]
                for line in lines:
                    phrases.add(line.rstrip().lower())

        return list(phrases)

    def words_from_files(filenames):
        """
        This method takes a list of file names and returns a list
        of unique words in those files.
        All phrases in files are broken down into individual words and added
        to the list.
        """

        if not filenames or type(filenames) is not list:
            print("DictionaryManager.words_from_files() Error :: argument 'filenames' must be a list.")
            return None

        words = set()
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = f.readlines()[1:]
                for line in lines:
                    for word in line.split():
                        words.add(word.rstrip().lower())

        return list(words)

    def shortest_len_in_dictionary(dictionary):
        """
        This method takes a list of words 'dictionary' and returns the length of
        the shortest word.
        """
        if not dictionary or type(dictionary) is not list:
            print("DictionaryManager.shortest_word_in_dictionary() Error :: argument 'dictionary' must be a list.")
            return None

        shortest_len = len(dictionary[0])
        for word in dictionary:
            word_len = len(word)
            if word_len < shortest_len:
                shortest_len = word_len

        return shortest_len

