# mlutils

Function utils to load work with datasets and models

## how to use it
clone the repository into your folder
```python
cd myproject
git clone https://github.com/nluninja/mlutils.git
```
import the module into your project, and call the needed utils

```python
import mlutils
```



## utils list

### model utils
Utils to work with models.

```python
compute_prediction_latency(dataset, model, n_instances=-1):
    """Compute prediction latency of a model.

def from_encode_to_literal_labels(y_true, y_pred, idx2tag):
    '''Transform sequences of encoded labels in sequences of string labels'''
```

### keras utils
Utils to load embeddings, to create LSTMs, and to memory usage: the memory functions work with Tensorflow only

```python
def get_model_memory_usage(batch_size, model):
    """Return memory usage of a model in MB given the batch size"""

def print_model_memory_usage(batch_size, model):
    """Print memory usage of a model in MB given the batch size"""

def load_glove_embedding_matrix(path, word_index, embed_dim):
    """Load Glove embeddings.    """

def load_w2v_nlpl_embedding_matrix(path, word_index, embed_dim):
    """Load NLPL Italian embedding."""

def create_BiLSTM(vocabulary_size, seq_len, n_classes, hidden_cells=128, 
                  embed_dim=32, drop=0.5, use_glove=False, glove_matrix=None):
    """Create a BiLSTM model using keras, given its parameters"""

def create_paper_BiLSTM(vocabulary_size, seq_len, n_classes, hidden_cells=200, 
                  embed_dim=100, drop=0.4, use_glove=False, glove_matrix=None):
    """Create a BiLSTM model using keras, given its parameters"""

def remove_flat_padding(X, y_true, y_pred, pad=0):
    """Remove padding predictions and flatten the list of sequences"""

def remove_seq_padding(X, y_true, y_pred, pad=0):
    """Remove padding predictions from list of sequences"""
```

### I/O utils
Utils to load datasets such as conll, wikiner.

```python
def open_read_from_url(url):
    """ Take in input an url to a .txt file and return the list of its raws"""

def read_raw_conll(url_root, dir_path, filename):
    """Read a file which contains a conll03 dataset"""

def is_real_sentence(only_token, sentence):
    """Chek if a sentence is a real sentence or a document separator"""

def load_conll_data(filename, url_root=CONLL_URL_ROOT, dir_path='', 
                    only_tokens=False):
    """ Take an url to the raw .txt files that you can find the repo linked above,
    load data and save it into a list of tuples data structure. """

def _df_to_xy(df):
    """Transform anerd dataframe in X, y sets."""

def load_wikiner(path, token_only=False):
    """Load WikiNER dataset."""

def _get_digits(text):
    """Preprocess numbers in tokens accordingly to itWac word embedding."""

def _normalize_text(word):
    """Preprocess word in order to match with the itWac embedding vocabulary"""

def itwac_preprocess_data(sentences):
    """Preprocess text in order to match with the itWac embedding vocabulary"""
```
