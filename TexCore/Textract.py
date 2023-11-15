class Textract:

    """
    Initialize the filepaths with the __init__ method.
    """
    def __init__(self, filepaths, chapters, aliases) -> None:
        self.filepaths = filepaths
        self.chapters = chapters
        self.aliases = aliases

        self.aliasCount = {}

        for filepath in filepaths:
            for key in self.aliases:
                self.aliasCount[(filepath, self.aliases[key])] = [0, []]

        self.__ExtractData()

    def __ExtractData(self):
        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                linecount = 1
                lines = file.read().splitlines()
                for line in lines:
                    self.__ProcessLine(line, linecount, filepath)
                    linecount += 1

    def __ProcessLine(self, line: str, linecount, filepath: str):
        for key in self.aliases:
            if (r'\begin' in line and self.aliases[key] in line) or (r'\end' in line and self.aliases[key] in line):
                self.aliasCount[(filepath, self.aliases[key])][0] += 1
                self.aliasCount[(filepath, self.aliases[key])][1].append(linecount)
