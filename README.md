# spelling-bee

Finds solutions to the New York Times' [Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) game.


## What is the Spelling Bee game?

Every day, the New York Times gives a set of 7 unique letters.  One of these letters is colored yellow.  The player must create words using as many or as few as these letters, as long as each word is at least 4 letters long and contains the yellow-colored letter.  The repetitions of the letters is permitted.  The goal of the game is to discover all valid English words that are possible using the allotted letters.


## How do I run the solver?

You must have Python 3 installed as well as the Numpy library.  If you have Anaconda installed, you can [install these dependencies](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) automatically using the provided `environment.yml` file.  With these dependencies installed, you can invoke the command `python solver.py` from the command line to run the script.


## How does the solver work?


### The trie

The goal of the Spelling Bee puzzle is to create words using an unordered set of letters and repetitions of letters are allowed.  So, to reference possible words that can be constructed using the provided letters, it is initially only necessary to know the unique letters in a valid word and not their order.  Thus, the program first pares each word in the English dictionary down to its unique letters and sorts them alphabetically.  Next, since many words in the dictionary share sequences of letters, the program builds a [prefix tree](https://en.wikipedia.org/wiki/Trie), also known as a *trie*, which enables multiple words to be identified simultaneously.  Once this tree has been created, the program stores it in a file so that whenever the program is next run, the tree already exists, thereby saving time.


### Using the trie to find words

To find valid words, the program first sorts the input letters alphabetically.  Then, it uses a depth-first traversal of the trie to find words using valid sets of letters.  Since it is possible for multiple words to exist at a given node and the program only generated parts of the tree that end in leaves containing words, searching the tree is much more efficient than using brute force to search word by word through the dictionary or to generated possible permutations of letters and test them against the dictionary.

