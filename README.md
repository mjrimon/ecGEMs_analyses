# ecGEMs_analyses
In this repository, you will find all the data and code needed to construct and analyze the Yeast9 ecGEMs based on Kcat predictions obtained using several different tools. This initial approach can be consulted here: https://github.com/jlott/kcat-prediction-benchmarking.

## data folder
Contains:
- Folder "yeast" with:
    - The predicted kcat dictionaries for the tools: CataPro, CatPred, DLKcat, MMKcat, TurNuP, UniKP.
    - The 10 kcat dictionaries from the CatPred results.
    - "mean" kcat dictionary.
    - Experimental kcat dictionary extracted from GECKO GitHub: https://github.com/SysBioChalmers/GECKO/tree/main/databases
- List of all predicted kcats.
- List of all reactions from Yeast9.
- The database used as input for the different kcat prediction tools.

## code folder
Contains:
- Growth notebook: For the construction of the ecGEMs with the different kcat dictionaries and their subsequent analyses plus the enviromental constrained GEM.
- pFBA notebook: for the pFBA analyses.

## model folder
Contains Yeast9 (v9.0.2) GEM from the yeast-GEM GitHub: https://github.com/sysbiochalmers/yeast-gem


[![DOI](https://zenodo.org/badge/1258336876.svg)](https://doi.org/10.5281/zenodo.20530152)
