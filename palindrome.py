from collections import defaultdict
import sys

def get_prefixes(word):
    return [word[:i] for i in range(len(word), 1, -1)]

def get_suffixes(word):
    return [word[i:] for i in range(1, len(word))]

def get_prefix_list(wordlist):
    """Returns prefix dictionary of wordlist"""

    prefixes = defaultdict(list)

    for word in wordlist:
        for i in range(1, len(word) + 1):
            prefixes[word[:i]].append(word[i:])

    return prefixes


def get_suffix_list(wordlist):
    """Returns suffix dictionary of wordlist"""

    suffixes = defaultdict(set)

    for word in wordlist:
        for i in range(len(word)):
            suffixes[word[i:]].add(word[:i])

    return suffixes


class PalindromeCounter:
    def __init__(self, max_palindromes):
        self.palindromes_left = max_palindromes
        self.palindromes_found = set()
    
    def print_palindrome(self, beginning, end):
        palindrome = ' '.join(beginning + end)
        if palindrome in self.palindromes_found:
            return
        
        print(palindrome)

        self.palindromes_left -= 1
        self.palindromes_found.add(palindrome)


def print_palindromes(first, wordlist, max_palindromes=50, max_words=30, min_len=0):
    wordlist = [w for w in wordlist if len(w) >= min_len]

    prefixes = get_prefix_list(wordlist)
    suffixes = get_suffix_list(wordlist)
    wordset = set(wordlist)

    counter = PalindromeCounter(max_palindromes)

    print_palindromes_with([first], [], first, '', wordset, prefixes, suffixes, counter, max_words)


def print_palindromes_with(beginning, end, front, back, wordset, prefixes, suffixes, counter, max_words):
    """
    Recursive helper method for print_palindromes

    beginning: words already set at the beginning of the palindrome
    end: words already set at the end of the palindrome
    front: front of the frontier; letters after the beginning that aren't part of a word yet
    back: back of the frontier; letters before the end that aren't part of a word yet
    """

    if counter.palindromes_left <= 0:
        return

    if len(beginning) + len(end) > max_words:
        return

    if not front and not back:
        counter.print_palindrome(beginning, end) # everything is matched
        return
    
    if front:
        front_rev = front[::-1]

        # if the front is a palindrome, we good
        if front == front_rev: 
            counter.print_palindrome(beginning, end)
        
        # find reverses of beginnings of front, if there are any
        for i in range(len(front), 0, -1):
            front_prefix = front[:i]
            new_front = front[i:]

            new_word = front_prefix[::-1]

            if new_word in wordset:
                print_palindromes_with(beginning, [new_word] + end, new_front, '', wordset, prefixes, suffixes, counter, max_words)
        
        # find words that end in the front reversed, if there are any
        if front_rev in suffixes:
            for new_back in suffixes[front_rev]:
                new_word = new_back + front_rev
                print_palindromes_with(beginning, [new_word] + end, '', new_back, wordset, prefixes, suffixes, counter, max_words)
    

    if back:
        back_rev = back[::-1]

        # if the back is a palindrome, we good
        if back == back_rev: 
            counter.print_palindrome(beginning, end)
        
        # find reverses of beginnings of back, if there are any
        for i in range(len(back)):
            back_suffix = back[i:]
            new_back = back[:i]

            new_word = back_suffix[::-1]

            if new_word in wordset:
                print_palindromes_with(beginning + [new_word], end, '', new_back, wordset, prefixes, suffixes, counter, max_words)
        
        # find words that start with the back reversed, if there are any
        if back_rev in prefixes:
            for new_front in prefixes[back_rev]:
                new_word = back_rev + new_front
                print_palindromes_with(beginning + [new_word], end, new_front, '', wordset, prefixes, suffixes, counter, max_words)


def main(args):
    with open('enable1.txt') as f:
        wordlist = f.read().splitlines()
        wordlist = [w.split(';')[0].upper() for w in wordlist]
    
    print_palindromes(args[1], wordlist, max_palindromes=50, max_words=10)


if __name__ == '__main__':
    main(sys.argv)