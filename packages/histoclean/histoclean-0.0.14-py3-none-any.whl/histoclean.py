import os
from tkinter import filedialog
import tkinter as tk
from back import image_patching, balance_module, whitespace_filter, image_normalisation, augmentation, patch_finder as pf
import initialisation

def SaveData():
    global Active_Module
    DefaultFile = [('HistoClean File', '*.hc')]
    SavePath = filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=DefaultFile, defaultextension=DefaultFile)
    print(f"Saving data to {SavePath}")
    Data = []

    if Active_Module == "Patch":
        Data.append("Patch")
        # Data.append(SettingValues)


def run():
    tk.mainloop()


def patch_image(imageFolder, saveLocation, outputTileSize, magnification, outputExtension):
    image_patching.ImagePatching.patch_image(imageFolder, saveLocation, outputTileSize, magnification, outputExtension)


def white_filter(imgFolder, minTissueCoverage, method, blur, keepSubThresholdImagesSeparate=1, createBinaryMasks=1):
    #  Needs the checkboxes at bottom added as parameters
    # This is done in gui using KeepCheckVar, which updates on checkbox update (needs checked)
    whitespace_filter.WhitespaceFilter.WS_Thread_Threading(imgFolder, minTissueCoverage, method, blur,
                                                           keepSubThresholdImagesSeparate, createBinaryMasks)

def balance(imgFolders, balance, folderVal):
    balance_module.Balance.Adjust_ProgressBar(imgFolders, balance, folderVal)

def image_normalisation(targetImage, targetFolder, method, newSaveFolder=None):
    image_normalisation.ImageNormalisation.Norm_Thread_Threading(targetImage, targetFolder, method, newSaveFolder)

def augment_images(imgFolder, augments, applySize, applyMethod):
    augmentation.Augmentation.augment(imgFolder, augments, applySize, applyMethod)


if __name__ == '__main__':
    run()