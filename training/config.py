## Use this file to specify the paths to your training data

# DATA PREPARATION

# Training Data Preparation Paths
MY_SOURCE_DIR   =       "./grammar_correction/my_text"          # Specify the source path to your correct grammar sentences
CLEAN_DIR       =       "./grammar_correction/cleaned_text"     # Specify the directory where you want your cleaned text to be saved
NOISY_PAIR_DIR  =       "./grammar_correction/noisy_pairs"      # Specify where you want your noisy pairs to be saved
SKIPPED_DIR     =       "./grammar_correction/skipped"          # Specify where you want skipped sentences to be logged to
DATASET_DIR     =       "./grammar_dataset"                     # Specify where you want the training dataset to be created

# Dataset config
MAX_WORDS       =       20                                      # Disgard sentences longer than this number (long sentences are not good for ASR grammar training)
MIN_WORDS       =       4                                       # Disgard sentences shorter than this number (short sentences are also not very useful for training)
CHUNK_SIZE      =       100000                                  # Reduce this is you are hitting RAM ceilings when you run create_dataset

# TRAINING CONFIG
CHECKPOINT_DIR  =       "./checkpoint"
TRAIN_BATCH     =       32
EVAL_BATCH      =       32
EPOCHS          =       10
STRATEGY        =       "epoch"
LOG_STEPS       =       100
SAVE_LIMIT      =       1
VARIANTS        =       ["t5-small", "t5-base", "t5-large"]     # remove model sizes that you do not wish to train
