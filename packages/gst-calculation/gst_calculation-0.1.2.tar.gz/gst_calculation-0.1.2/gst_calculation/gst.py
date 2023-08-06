"""GST is a module that calculates Greedy String Tiling algorithm as described in
"String Similarity via Greedy String Tiling and Running Karp−Rabin Matching"
(Wise, 1993)
Source: https://www.researchgate.net/publication/262763983_String_Similarity_via_Greedy_String_Tiling_and_Running_Karp-Rabin_Matching.

    Typical usage example:

    from gst_calculation import gst
    gst_result = gst.calculate(sequence_1,sequence_2,5)
    
    # total of same tiles
    total_score = gst_result[1]
"""

def initialize_status(tokens):
    """Initialize all tokens to False or Unmarked.

    Args:
        tokens (list): A list of pair of strings and it's status.

    Returns:
        list: The returned list contains pair list of every token with False boolean.
    """
    tokens_status = []
    
    #initialize all tokens to False / unmarked
    for token in tokens:
        tokens_status.append([token,False])
    
    return tokens_status


def compare_token(tokens1, tokens2, line_1_num, line_2_num, same_tokens):
    """Compare tokens and makes sure both of them have False status.

    Args:
        tokens1 (list): A list of pair of strings and it's status.
        tokens2 (list): A list of pair of strings and it's status.
        line_1_num (int): The index of token from tokens1 that are currently checked.
        line_2_num (int): The index of token from tokens2 that are currently checked.
        same_tokens (int): The amount of same tokens for both tokens from the starting token.

    Returns:
        boolean: True if both of the token have the same value and unmarked (False status)
    """
    try:
        #check if both token are the same token
        if tokens1[line_1_num + same_tokens] == tokens2[line_2_num + same_tokens]:
            
            #check if both token are unmarked
            if tokens1[line_1_num + same_tokens][1] == tokens2[line_2_num + same_tokens][1] == False:
                return True
    
    # return False if the index is not accesible
    except:
        return False
    
    # return false if both condition are not satisfied
    return False          


# to verify same length matches don't overlay
def check_same_length_match(matches, line_1_num, line_2_num):
    """Checks for cases if found token with same length as the current max_match. 
    This is needed to make sure the new match is new and doesn't overlap the existing matches.

    Args:
        matches (list): A list of matches list, match list contains
            [line_1_num, line_2_num, same_tokens].
        line_1_num (int): The index of token from tokens1 that are currently checked.
        line_2_num (int): The index of token from tokens2 that are currently checked.

    Returns:
        boolean: True if both line_1_num doesn't exist in existing matches.
    """
    for line_3_num, match in enumerate(matches):
        match_line_1_start = match[0]
        match_line_2_start = match[1]
        match_len = match[2]

        # if overlap with tokens1
        if line_1_num >= match_line_1_start and line_1_num <= match_line_1_start + match_len - 1:
            return False
        
        # if overlap with tokens2
        if line_2_num >= match_line_2_start and line_2_num <= match_line_2_start + match_len - 1:
            return False

    return True



def calculate(tokens_sequence_1, tokens_sequence_2, minimal_match = 3):
    """Calculates greedy string tiling from both of token sequence.

    Args:
        tokens_sequence_1 (list): A list of strings. 1 string equals to 1 token.
        tokens_sequence_2 (list): A list of strings. 1 string equals to 1 token.
        minimal_match (int): Bottom limit / Number of minimal consecutively 
            equal tokens that considered to be a tile.

    Returns:
        list: The first index will be a list of tiles that contains match dict.
            Match dict will contain 4 keys ('token_1_position', 'token_2_position', 'length', 'score')
            'token_1_position' = starting position for tokens_sequence_1
            'token_2_position' = starting position for tokens_sequence_2
            'length' = length of matched / same tokens (starting position + 'length' would be the ending position)
            'score' = score of the match, 1 token matched equals to 1 score.

            The second index will be total score. The total score is accumulative score of matched tiles.
    """
    same_tiles = []
    total_score = 0

    tokens_1 = initialize_status(tokens_sequence_1)
    tokens_2 = initialize_status(tokens_sequence_2)

    switched = False
    # optimization - shorter array should be base for comparison
    if len(tokens_2) < len(tokens_1): 
        tokens_1, tokens_2 = tokens_2, tokens_1
        switched = True

    max_min=True

    while(max_min):
        max_match = minimal_match
        matches = []
        for line_1_num, [token1,is_match_1] in enumerate(tokens_1):
            if not is_match_1:
                for line_2_num, [token2,is_match_2] in enumerate(tokens_2):
                    if not is_match_2:
                        same_tokens = 0
                        while compare_token(tokens_1, tokens_2, line_1_num, line_2_num, same_tokens):
                            same_tokens += 1

                        # if found same length match, check first if it's overlapping or not
                        if same_tokens == max_match:
                            if check_same_length_match(matches, line_1_num, line_2_num):
                                matches.append([line_1_num, line_2_num, same_tokens])

                        # if found longer match, replace the current match with longer one
                        elif same_tokens > max_match:
                            max_match = same_tokens
                            matches = [[line_1_num, line_2_num, same_tokens]]

        for match in matches:
            for enumerate_length in range(match[2]):
                # mark the token as True / already becomes a tile
                tokens_1[match[0] + enumerate_length][1] = True
                tokens_2[match[1] + enumerate_length][1] = True

            tile = {
                'token_1_position': match[0],
                'token_2_position': match[1],
                'length': match[2],
                'score': match[2]
            }

            total_score += match[2]
            same_tiles.append(tile)

        # if the max match is still bigger than the minimal_match, then repeat the search for the rest of unmarked tokens
        if max_match <= minimal_match:
            max_min = False

    # #reverse if switched at the initialization
    if switched:
        for tile in same_tiles:
            tile['token_1_position'], tile['token_2_position'] = tile['token_2_position'], tile['token_1_position']
    
    return [same_tiles, total_score]
                