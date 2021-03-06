import multiprocessing
import string

from map_reduce import SimpleMapReduce

def word_to_letters(word):
    """Read a word and return a sequence of (letter, occurances) values.
    """

    output = []
    if word.isalpha():
        word = word.lower()
        for letter in word:
            output.append( (letter, 1) )
    return output


def count_letters(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    letter, occurances = item
    return (letter, sum(occurances))


if __name__ == '__main__':
    import glob
    import operator
    import time

    processList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    input_files = glob.glob('*.txt')

    TR = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

    texts = ''
    for filename in input_files:
        with open(filename, "r") as f:
            for line in f:
                texts = texts + line.translate(TR)

    for processes in processList:
        for _ in range(10):
            mapper = SimpleMapReduce(word_to_letters, count_letters, processes)
            start_time = time.time()
            letter_counts = mapper(texts.split())
            end_time = time.time()
            print "{0}\t{1}".format(processes, end_time - start_time)

#    letter_counts.sort(key=operator.itemgetter(1))
#    letter_counts.reverse()

#    print '\nTOP LETTERS BY FREQUENCY\n'
#    longest = max(len(letter) for letter, count in letter_counts)
#    for letter, count in letter_counts:
#        print '%-*s: %8s' % (longest+1, letter, count)
