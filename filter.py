class Filter():

    def terms_from_files(filenames):
        """
        This method takes a list of file names and returns a list
        of unique terms in those files.
        """

        if not filenames or type(filenames) is not list:
            print("Filter.terms_from_files() Error :: argument 'filenames' must be a list.")
            return None

        terms = set()
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = f.readlines()[1:]
                for line in lines:
                    terms.add(line.rstrip().lower())

        return list(terms)
