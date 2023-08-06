# GST Calculation
GST is a module that calculates Greedy String Tiling algorithm as described in "String Similarity via Greedy String Tiling and Running Karp−Rabin Matching" (Wise, 1993) - https://www.researchgate.net/publication/262763983_String_Similarity_via_Greedy_String_Tiling_and_Running_Karp-Rabin_Matching

# Installation
### Using PIP via PyPI
```
pip install gst-calculation
```
### Using PIP via Github
```
pip install git+https://github.com/tomytw/gst-calculation.git@0.1.2
```

# Usage

## Importing the package
```
>>> from gst_calculation import gst
```
You can calculate a gst of a collection of numbers or strings (or any collection of object that can be compared using equal function, must have \_\_eq\_\_ method inside it's class)

The result will be array that contains two elements (two index):
1. Tile information (position and length of matched tiles)
2. Total score
## GST on Numbers List
```
>>> tokens_sequence_1 = [1,2,3,4,5]
>>> tokens_sequence_2 = [3,4,5,6,7]
>>> gst.calculate(tokens_sequence_1, tokens_sequence_2, minimal_match=3)
    [[{'token_1_position': 2, 'token_2_position': 0, 'length': 3, 'score': 3}], 3]
```
## GST on Strings List
```
>>> tokens_sequence_1 = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
>>> tokens_sequence_2 = ['the', 'lazy', 'dog', 'jumps', 'over', 'the', 'quick', 'brown', 'fox']
>>> gst.calculate(tokens_sequence_1, tokens_sequence_2, minimal_match=3)
    [[{'token_1_position': 0, 'token_2_position': 5, 'length': 4, 'score': 4},
    {'token_1_position': 6, 'token_2_position': 0, 'length': 3, 'score': 3}],
    7]
```



