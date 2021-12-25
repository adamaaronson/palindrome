from collections import defaultdict
import sys

def get_prefixes(word):
    return [word[:i] for i in range(len(word), 0, -1)]

def get_suffixes(word):
    return [word[i:] for i in range(len(word))]

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


def make_palindrome(first, wordlist, maxwords=30, minlen=0):
    """Returns a palindrome starting with the given first word using the words in wordlist"""
    wordlist = [w for w in wordlist if len(w) >= minlen]

    prefixes = get_prefix_list(wordlist)
    suffixes = get_suffix_list(wordlist)
    wordset = set(wordlist)

    return make_palindrome_with([first], [], first, '', wordset, prefixes, suffixes, maxwords)


def make_palindrome_with(beginning, end, front, back, wordset, prefixes, suffixes, maxwords):
    """
    Recursive helper method for make_palindrome

    beginning: words already set at the beginning of the palindrome
    end: words already set at the end of the palindrome
    front: front of the frontier; letters after the beginning that aren't part of a word yet
    back: back of the frontier; letters before the end that aren't part of a word yet
    """

    # print(beginning, end, front, back)

    if len(beginning) + len(end) > maxwords:
        return None

    if not front and not back:
        return beginning + end # everything is matched
    
    if front and back:
        return None # this shouldn't happen I think
    
    if front:
        front_rev = front[::-1]

        # if the front is a palindrome, we good
        if front == front_rev: 
            return beginning + end
        
        # find reverses of beginnings of front, if there are any
        for i in range(len(front), 0, -1):
            front_prefix = front[:i]
            new_front = front[i:]

            new_word = front_prefix[::-1]

            if new_word in wordset:
                result = make_palindrome_with(beginning, [new_word] + end, new_front, '', wordset, prefixes, suffixes, maxwords)

                if result:
                    return result
        
        # find words that end in the front reversed, if there are any
        if front_rev in suffixes:
            for new_back in suffixes[front_rev]:
                new_word = new_back + front_rev
                result = make_palindrome_with(beginning, [new_word] + end, '', new_back, wordset, prefixes, suffixes, maxwords)

                if result:
                    return result
    

    if back:
        back_rev = back[::-1]

        # if the back is a palindrome, we good
        if back == back_rev: 
            return beginning + end
        
        # find reverses of beginnings of back, if there are any
        for i in range(len(back)):
            back_suffix = back[i:]
            new_back = back[:i]

            new_word = back_suffix[::-1]

            if new_word in wordset:
                result = make_palindrome_with(beginning + [new_word], end, '', new_back, wordset, prefixes, suffixes, maxwords)

                if result:
                    return result
        
        # find words that start with the back reversed, if there are any
        if back_rev in prefixes:
            for new_front in prefixes[back_rev]:
                new_word = back_rev + new_front
                result = make_palindrome_with(beginning + [new_word], end, new_front, '', wordset, prefixes, suffixes, maxwords)

                if result:
                    return result
    
    return None


def main(args):
    with open('enable1.txt') as f:
        wordlist = f.read().splitlines()
        wordlist = [w.split(';')[0].upper() for w in wordlist]
    
    palindrome = make_palindrome(args[1], wordlist, minlen=3)

    if palindrome:
        print(' '.join(palindrome))
    else:
        print('No palindrome found. :(')


if __name__ == '__main__':
    main(sys.argv)