
==================================================

Multi Word Expression (MWE) detection task project

==================================================

This project uses machine learning models aiming to classify MWEs - multiple words with a property that 
the meaning of the whole is not derived from the meaning of its parts. 
By using publicly available datasets of various languages from the [PARSEME Shared Task](https://typo.uni-konstanz.de/parseme/) 
ver.1.1, we try out machine learning techniques (Support vector machine, Random forest) and compare their accuracy in correctly 
detecting different MWEs categories.

The repository contains python code which pre-processes the PARSEME datasets (generate\_cupts.py), exports the data sets as 
raw text files (generate_rawtext.py), the training script (training.py), and config file (settings.py). 
Word vector models used for text-to-vector representation for the training were downloaded from [here:](https://fasttext.cc/docs/en/pretrained-vectors.html). 

The script expects the word vector models in the .vec text format and loads it to a 
dictionary when running, eliminating the need to have fastText library installed.

----- Requirements ------

-python3.6

-scikit-learn

-numpy

-------------------------