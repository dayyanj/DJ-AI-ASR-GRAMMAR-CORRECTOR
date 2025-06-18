Data Preparation Instructions:

Training data is prepared by taking gramatically correct short sentences, stripping them of any non ASR artifacts and general clean up to match ASR style output, parsing them through noise functions to generate noisy/correct pairs and building the dataset for use in training.

The helper modules in this directory are designed to speed up the creation of your datasets.

Modules:
training>data_preparation>clean_text.py
This module iterates through text files in the specified folder and performs cleanup on the inputs (removes non ASR like artifacts), splits sentences over new lines and outputs to the cleaned_output directory

training>data_preparation>create_noisy_pairs.py
This module handles converting your cleaned_text into incorrect/correct pairs by applying randomised ASR like error generating functions against each line. Where no ASR errors can be generated or where the sentance is too long or two short, they will be excluded from the final noisy_pair data.

training>data_preparation>noise_functions.py
This module holds all of the functions used to generate ASR styled errors. It is called by create_noisy_pairs.py and does not need to be used indirectly.

training>data_preparation>create_dataset.py
This module takes the noisy pairs created by create_noisy_pairs.py and prepares them as your training dataset.

Before the dataset is created your data should look like the following examples, with incorrect ASR like errors <TAB> Correct output.

----------------------
an does the book interest a you?	Does the book interest you?
he doesn't a have a an car.	He does not have a car.
she did not go go for school today.	She did not go to school today.
you be going to the beach tomorrow.	We are going to the beach tomorrow.

----------------------

INSTRUCTIONS:

Step 1. Get your data set ready:
prepare a file with all of your correct grammar. Each sentence should be on it's own line and be gramatically correct with appropriate casing. E.g. "Does the book interest you?" (without quotes).

