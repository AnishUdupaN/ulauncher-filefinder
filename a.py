def match_score(word, keyword):
    """Calculate number of common letters between word and keyword."""
    word_letters = set(word)
    keyword_letters = set(keyword)
    return len(word_letters & keyword_letters)

def sort_by_match(words, keyword):
    """Sort words based on match score in descending order."""
    return sorted(words, key=lambda word: match_score(word, keyword), reverse=True)

# Example usage:
words_list = ["home/anishudupan/projects/ul-z","zzlluu","uullzz","home/anishudupan/projects/ulauncher-filefinder","apple", "banana", "grape", "orange", "peach"]
keyword = "ulz"

sorted_words = sort_by_match(words_list, keyword)
print("Sorted words:", sorted_words)
