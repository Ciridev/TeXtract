from enum import Enum
import pandas as pd
import math
import os

class Status(Enum):
    Ok = 0
    FileNotFound = 1
    Mismatch = 2
    OverlapValue = 3
    OverlapKey = 4

"""
Class used to load Data from files.
"""
class Loader:
    """
    Variables Used:
        - data: The raw pandas DataFrame.
        - aliases: A dictionary containing the aliases for the book sections.
        - chapters: A dictionary containing the chapter names, and their numbering. 
        - status: Keeps track of the status of the data loading.
    """

    def __init__(self) -> None:
        self.aliases = {}
        self.chapters = {}
        self.filepaths = []
        self.status = Status.Ok
    
    """
    Load the csv file containing project information: 
        - Theorems, Lemmas, etc. Aliases
        - Chapters numbering

    The csv must be written row-major, because it's most likely 
    uneven. For this reason, it is performed a DataFrame transposition
    after the instantiation of the data.
    """
    def LoadSetupData(self, filepath) -> Status: 
        try:
            self.data = pd.read_csv(filepath, header=None)
        except: 
            self.status = Status.FileNotFound 
            return    
        
        self.data = self.data.transpose()
        self.data.columns = ['Aliases','Chapter name', 'Numbering']
        
        # Initialize collected data
        aliasCol    = self.data['Aliases']
        chapNameCol = self.data['Chapter name']
        numbCol     = self.data['Numbering']

        for alias in aliasCol:
            aliasList = alias.split('.', 1)
            self.aliases[aliasList[0].replace('"', '').strip()] = aliasList[1].replace('"', '').strip()
    
        counter = 0
        chapterNan = 0
        numberNan = 0
        for numb in numbCol:
            try:
                if math.isnan(float(chapNameCol[counter])):
                    chapterNan += 1
                if math.isnan(float(numb)):
                    numberNan += 1
            except:
                if int(numb) in self.chapters:
                    self.status = Status.OverlapKey
                    return self.status
                
                if chapNameCol[counter].replace('"', '').strip() in self.chapters.values():
                    self.status = Status.OverlapValue
                    return self.status

                self.chapters[int(numb)] = chapNameCol[counter].replace('"', '').strip()
                counter += 1

        if chapterNan != numberNan:
            self.status = Status.Mismatch

        self.chapters = dict(sorted(self.chapters.items()))

        return self.status

    """
    Store the chapters filepaths and prepare them to be sent
    to the TeXtract class.
    """
    def SetupChaptersMetadata(self, directory) -> list[str]:
        os.chdir(directory)
        for filename in os.listdir('.'):
            if filename.endswith('.tex'):
                self.filepaths.append(os.path.abspath(filename))

        os.chdir('..')
        return self.filepaths

    # "Alias", "Chapter Name", "Numbering"
