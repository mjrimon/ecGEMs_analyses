# ecGEMs_analyses
In this repository you will find all the data and code necessary to construct and analyze the ecGEMs used in the paper: 

"Are machine-learning \kcat predictors ready for systems biology applications? Benchmark performance does not reliably translate into improved enzyme-constrained metabolic models".

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
- pFBA notebook: for the pFBA analyses showed in the paper.

## model folder
Contains Yeast9 GEM from the yeast-GEM GitHub: https://github.com/sysbiochalmers/yeast-gem

