import TexCore as tx
import pandas as pd
import os

"""
C-Style programming goes brr
"""

def main():
    """
    Get the absolute path of the setup.csv file
    and load the content in the tx.Loader class.
    """
    setupPath = os.path.abspath("setup.csv")
    loaderObj = tx.Loader()
    status = loaderObj.LoadSetupData(setupPath)

    if status == tx.Status.Mismatch: 
        print(f'Chapter name/numbering mismatch! Check your setup file!')
        return
    
    if status == tx.Status.FileNotFound: 
        print("File not found!")
        return

    if status == tx.Status.OverlapKey:
        print('Two chapters have the same numbering! Check your setup file!')
        return
    
    if status == tx.Status.OverlapValue:
        print('A chapter has been assigned twice! Check your setup file!')
        return

    # print(loaderObj.data, loaderObj.chapters, loaderObj.aliases)

    filepaths = loaderObj.SetupChaptersMetadata(directory='Chapters')
    textractObj = tx.Textract(filepaths, loaderObj.chapters, loaderObj.aliases)
    
    print(textractObj.aliasCount)

if __name__ == "__main__":
    main()

