import regex as re
import pandas as pd
from rapidfuzz import fuzz

def keyword_context(content, terms, file_name, 
                                        words_before=250, words_after=250, words_around=50, match_threshold=80):
    """
    Finds terms within a document, capturing approximate matches and customizable context.
    - Matches are determined based on a similarity threshold.

    Parameters:
    - content (str): The content of the document.
    - terms (list): List of search terms.
    - file_name (str): Name of the file being processed.
    - words_before (int): Number of words to capture before the term (including the term).
    - words_after (int): Number of words to capture after the term (including the term).
    - words_around (int): Number of words to capture around the term (split evenly before and after).
    - match_threshold (int): Minimum similarity score (0-100) for a word to be considered a match.

    Returns:
    - pd.DataFrame: A DataFrame with details about found terms and their customized context.
    """
    # Treat the entire content as a single page
    pages = [content]
    results = []

    for page_number, page_content in enumerate(pages, start=1):
        word_list = page_content.split()

        for word_index, word in enumerate(word_list):
            # Check for approximate matches with all terms
            for term in terms:
                similarity = fuzz.ratio(word.lower(), term.lower())
                if similarity >= match_threshold:  # Match found
                    # Extract contexts
                    previous_context = " ".join(word_list[max(0, word_index-words_before):word_index+1])
                    next_context = " ".join(word_list[word_index:min(len(word_list), word_index+words_after+1)])
                    around_context = " ".join(word_list[max(0, word_index-words_around//2):min(len(word_list), word_index+(words_around//2)+1)])
                    
                    # Append result
                    results.append({
                        "File Name": file_name,
                        "Page Number": page_number,
                        "Matched Term": word,
                        "Original Term": term,
                        "Similarity Score": similarity,
                        f"Search Term with {words_around} Words Context": around_context.strip(),
                        f"Previous {words_before} Words (Including Term)": previous_context.strip(),
                        f"Next {words_after} Words (Including Term)": next_context.strip(),
                    })

    if not results:
        print("No results found!")
        return None

    
    return pd.DataFrame(results)