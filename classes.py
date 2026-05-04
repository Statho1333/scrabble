import itertools as it
import json
import random
from collections import Counter
from abc import ABC, abstractmethod

class Game():

    def __init__(self):
        self.sak = SakClass()
        self.wordsSet = self.loadWords()
        self.human = None
        self.computer = None
        self.onGoingGame = False



    def showStartingInterface(self):

        choices = ('1','2','3','q')

        humanName = input('Το όνομά σου είναι: ')
        self.human = Human(humanName)


        while True:

            print(f'***** SCRABBLE ******')
            print(f'1: Σκορ')
            print(f'2: Ρυθμίσεις')
            print(f'3: Παιχνίδι')
            print(f'q: Έξοδος')

            choice = input()

            while True:
                if choice not in choices:
                    print(f'Μη αποδεκτή απάντηση. Πρέπει να επιλέξετε μία από τις παρακάτω επιλογές')
                    print(f'***** SCRABBLE ******')
                    print(f'1: Σκορ')
                    print(f'2: Ρυθμίσεις')
                    print(f'3: Παιχνίδι')
                    print(f'q: Έξοδος')
                    choice = input()
                else:
                    break
            
            match choice:
                case '1':
                    self.showScore()
                case '2':
                    self.setup()
                case '3':
                    self.run()
                case 'q':
                    self.end()

    def showScore(self):
        print(f'{self.human.name} score is: {self.human.getScore()}')
        print(f'{self.computer.name} score is: {self.computer.getScore()}')


    def setup(self):
        choices = ('1','2','3','b')

        while True:
            print(f'***** ΕΠΙΛΕΞΤΕ ΑΝΤΙΠΑΛΟ *****')
            print(f'Επιλέξτε έναν από τους παρακάτω αντιπάλους-ρομπότ!')
            print(f'1: C3PO Human Cyborg Relationships. Droid το οποίο γνωρίζει πάνω από 6 εκατομμύρια μορφές επικοινωνίας. Μεταξύ μας δεν είναι και πολύ έξυπνο')
            print(f'2: R2D2. Droid το οποίο δεν μιλάει αρκετά παράξενα αλλά είναι εμφανές πιο έξυπνο από τον C3PO')
            print(f'3: BB-8. Το πιο έξυπνο από όλα τα droids')
            print(f'b: Επιστροφή στο αρχικό menou')

            choice = input()

            while True:
                if choice not in choices:
                    print(f'Λάθος επιλογή, επιλέξτε έναν από τους παρακάτω αντιπάλους-ρομποτ.')
                    print(f'1: C3PO Human Cyborg Relationships. Droid το οποίο γνωρίζει πάνω από 6 εκατομμύρια μορφές επικοινωνίας. Μεταξύ μας δεν είναι και πολύ έξυπνο')
                    print(f'2: R2D2. Droid το οποίο δεν μιλάει αρκετά παράξενα αλλά είναι εμφανές πιο έξυπνο από τον C3PO')
                    print(f'3: BB-8. Το πιο έξυπνο από όλα τα droids')
                    print(f'b: Επιστροφή στο αρχικό menou')
                    choice = input()
                else:
                    break
            
            if choice == 'b':
                return
            else:
                match choice:
                    case '1':
                        computerName = 'C3PO'
                        algo = 'min'
                    case '2':
                        computerName = 'R2D2'
                        algo = 'max'
                    case '3':
                        computerName = 'BB-8'
                        algo = 'smart'
                
                self.computer = Computer(self.computerName, algo)
                return


    def loadWords(self) -> set:
        try:
            with open('greek7.txt', 'r', encoding='utf-8') as f:
                return {line.strip() for line in f}
        except FileNotFoundError:
            print('Το αρχείο δεν βρέθηκε')
            return set()
        
    def refillHand(self,player : Player):
        needed = min(7-len(player), len(self.sak))
        player.hand+= self.sak.getLetters(needed)

    def run(self):     
        if self.computer is None:
            self.computer = Computer('C3PO', 'min')

        while True:
            humanCanPlay = False
            computerCanPlay = False

            #HUMAN ACTIONS
            while True:
                self.human.__repr__()
                print(f'Αν θέλεις να αλλάξεις τα γράμματά σου, πληκτρολόγησε "P"')
                print(f'Αν θέλεις να παραιτηθείς πληκτρολόγησε "Q"')
                print(f'Αν θέλεις να παίξεις, απλά πληκτρολόγησε την λέξη σου')
                word = input('ΛΕΞΗ Ή ΕΠΙΛΟΓΉ: ').upper()
                response, option = self.human.play(word,self.wordsSet)

                if not response and option == 'Change':
                    if len(self.sak) == 0:
                        print(f'Δεν υπάρχουν άλλα γράμματα για αλλαγή, χάνεις την σειρά σου')
                    else:
                        self.sak.putBackLetters(self.human.hand)
                        self.human.hand = []
                        self.refillHand(self.human)
                    break
                elif not response and option == 'End':
                    self.end()
                elif response and option == 'Valid':
                    humanCanPlay = True
                    score = self.human.calculateScore(word)
                    self.human.addScore(score)
                    self.human.hand = self.human.hand - list(word)
                    self.refillHand(self.human)
                    print(f'Πόντοι λέξης: {score}')
                    self.human.__repr__()
                    break
                else:
                    print(f'Δεν υπάρχει η λέξη που πληκτρολόγησες, προσπάθησε ξανά!')

            #Computer actions
            self.computer.__repr__()
            computerWord, computerScore = self.computer.play(self.wordsSet)
            if computerWord is None:
                if len(self.sak) == 0:
                    self.end()
                else:
                    print(f'{self.computer.name} δεν βρήκε λέξη, αλλάζει γράμματα!')
                    self.sak.putBackLetters(self.computer.hand)
                    self.computer.hand = []
                    self.refillHand(self.computer)
            else:
                computerCanPlay = True
                self.computer.addScore(computerScore)
                self.computer.hand = self.computer.hand - list(computerWord)
                self.refillHand(self.computer)
                print(f'Πόντοι λέξης: {computerScore}')
                self.computer.__repr__()

            if self.isGameOver(humanCanPlay, computerCanPlay):
                self.end()


    def isGameOver(self, humanCanPlay: bool, computerCanPlay: bool) -> bool:
        if not humanCanPlay and not computerCanPlay:
            return True
        if len(self.sak) == 0 and len(self.human) == 0:
            return True
        if len(self.sak) == 0 and len(self.computer) == 0:
            return True
        return False

    def end(self):
        pass


    


class SakClass():
    """
    Class that represents the bag of letters, containing 104 greek letters.

    Attributes:
    - lets: A dictionary represanting the occurances of each letter and the points of the letters, if used in a word

    Example:
    - "A" : [12,1] -> letter "A" is 12 times in the sak, awarding 1 point.
    """

    lets = {'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],
        'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],
        'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],
        'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],
        'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3]
        }
    
    def __init__(self):
        """
        Constructor of SakClass.
        Randomizes a sak.
        """
        self.sak = self.randomizeSak(SakClass.lets)

    #takes as input a random dictionary of letters, flattens it and shuffles it
    def randomizeSak(self, letters: dict) -> list:
        """
        Function that flattens the letters dictionary, converting it to a string, and shuffles it,cdepending on the occurences of each letter

        Attributes:
        - letters: the class attribute lets dictionary

        Returns:
        sak: a shuffled list of letters
        """
        sak = [letter for letter, (count, points) in letters.items() for _ in range(count)]
        random.shuffle(sak)
        return sak

    #removes n letters from sak
    def getLetters(self, n: int) -> list:
        """
        Function that removes n number of letters from the sak object.

        Parameters:
        - n: int, the number of letters to remove

        Return: a list of length n random letters from sak.
        """
        letters = self.sak[:n]
        self.sak = self.sak[n:]
        return letters
    
    #places back the letters, expecting a list to be given
    def putBackLetters(self,letters: list[str]):
        """
        A function that concats sak list with a given list containing str's that represent letters

        Parameters:
        - letters: list[str] representing letters

        -Returns:
        The self.sak shuffled

        Example:
        sak = [a,b,c], letters = [d,e,f] -> self.sak = [c,a,d,f,e,b]
        """
        self.sak.extend(letters)
        random.shuffle(self.sak)

    #returns the len of the sak
    def __len__(self) -> int:
        """
        Overloads build in len() function

        Returns:
        The length of the sak object (how many letters contains the list sak)
        """
        return len(self.sak)


class Player():
    """
    Basic class of players, from which derives Human and Computer

    """
    def __init__(self, name):
        """
        Attributes:
        - name: name of the player
        - hand: a list of letters representing the scrabble letter tiles
        - score: the score that the player has gathered
        """
    
        self.name = name
        self.hand = []
        self.score = 0

    def __repr__(self):
        """
        Prints basic information for the player, such as the name, the score and the list of the hand
        """
        print(f'******************************************************************')
        print(f'*** Παίκτης: {self.name} *** Σκορ: {self.getScore()}')
        print(f'Γράμματα: {self.hand}')
        print(f'\n*****************************************************************')

    def getScore(self):
        """
        Getter for score
        """
        return self.score
    
    def addScore(self,points):
        """
        Adds points to the score of the player
        """
        self.score+=points

    def calculateScore(self,word: str) -> int:
        """
        Calculates the points of a word

        Returns:
        -int: the sum of the letters

        Example:
        - H=8, I=2, calculateScore('hi') = 10
        """
        return sum(SakClass.lets.get(letter)[1] for letter in word)
    
    def __len__(self):
        """
        Overloads the build in len() function, to return the length of the hand of a player
        
        Returns:
        - int: the length of the self.hand
        """
        return len(self.hand)
    
    def __sub__(self,word: str):
        """
        Overloads subtraction operator. Removes a sub list from a list

        Returns: 
        - self: a new list, without the letters of the word given

        Example:
        -[b,a,n,a,n,a] - 'anna' -> [b,a]

        """
        newHand = self.hand.copy()
        for letter in word:
            newHand.remove(letter)
        self.hand = newHand
        return self
    
    @abstractmethod

    def play(self,sak,word_set):
        pass



class Human(Player):
    """
    Class that represents a human player. Inherits attributes and functions from Player Class.
    Calls the init function of the Player class
    """
    def __init__(self,name):
        """
        Constructor of the class.

        Attributes:
        - name: The name of the player
        """
        super().__init__(name)

    def isValidWord(self,word: str) -> bool:
        """
        Checks if a word can be produced from the hand of the player

        Parameters:
        - word: the str to check

        Returns:
        - True if str can be produced from hand, False otherwise

        -Example:
        - 'anna' , [b,a,n,a,n,a] -> True
        """
        return Counter(word)<= Counter(self.hand)

    def play(self, word:str, validWords: set) -> set:
        """
        Overides play function from Player Class. Checks what action the Player is gonna pick.

        Parameteres:
        - word: string to play
        - validWords: set of valid words (from 'gree7.txt')

        Returns:
        - False, 'Change': if 'P' was given as parameter from the word arg
        - False, 'End': if 'Q' was given as parameter from the word arg
        - True, 'Valid': if word can derive from hand and it is a word of the greek lang
        - True, 'Invalid': if either word cant derive from hand or is not a word from the greek lang
        """
        match word:
                case 'P':
                    return False, 'Change'
                case 'Q':
                    return False, 'End'
                case _:
                    if word in validWords and self.isValidWord(word):

                        return True, 'Valid'
                    return True, 'Invalid'

class Computer(Player):
    """
    Class that represents the computer player. Inherits attributes and functions from Player Class
    """
    def __init__(self, name='C3PO'):
        """
        Constructor of the class. Default value for name = 'C3PO'. Sets the difficulty of the game

        Attributes:
        - name: the name of the droid
        - mode: the difficulty of the game. Difficulty is from algo's Min, Max, Smart
        """
        super().__init__(name)
        self.mode = self.pickMode(self.name)

    def pickMode(self, name: str) -> str:
        """
        Sets the difficulty of the game, based from the droid name

        Parameteres:
        - name: str that represents the name of the droid

        Returns:
        - "min": if the given name was "C3PO" (easy difficulty)
        - "max": if the given name was "R2D2" (medium difficulty)
        - "smart": if the given name was "BB-8" (hard difficulty)
        """
        match name:
            case 'C3PO':
                return 'min'
            case 'R2D2':
                return 'max'
            case 'BB-8':
                return 'smart'
            
    def minLetters(self,validWords: set) -> tuple:
        """
        Implements the "Min" algorithm. Finds the smallest valid word that is part of the greek language and can derive from the computer's hand.

        Parameters:
        -validWords: the words of the greek alphabet

        Returns:
        - (word, score): The word that was created and the score of the word
        - (None, 0): if no word could derive
        """
        for length in range(2,len(self.hand)+1):
            for perm in it.permutations(self.hand,length):
                word = ''.join(perm)
                if word in validWords:
                    return word, self.calculateScore(word)
        return None, 0

    def maxLetters(self,validWords: set) -> tuple:
        """
        Implements the "Max" algorithm. Finds the biggest valid word that is part of the greek language and can derive from the computer's hand.

        Parameters:
        -validWords: the words of the greek alphabet

        Returns:
        - (word, score): The word that was created and the score of the word
        - (None, 0): if no word could derive
        """
        for length in range(len(self.hand), 1, -1):
            for perm in it.permutations(self.hand, length):
                word = ''.join(perm)
                if word in validWords:
                    return word, self.calculateScore(word)
        return None, 0

    def smart(self,validWords: set) -> tuple:
        """
        Implements the "Smart" algorithm. Finds the valid word with the most points that is part of the greek language and can derive from the computer's hand.

        Parameters:
        -validWords: the words of the greek alphabet

        Returns:
        - (word, score): The word that was created and the score of the word
        - (None, 0): if no word could derive
        """
        bestWord = None
        bestScore = 0
        for length in range(len(self.hand),1,-1):
            for perm in it.permutations(self.hand,length):
                word = ''.join(perm)
                if word in validWords:
                    score = self.calculateScore(word)
                    if score > bestScore:
                        bestScore = score
                        bestWord = word
        return bestWord, bestScore
    
    def play(self, word_set: set):
        """
        Executes the Min, Max or Smart algorithm, depending on the picked mode

        Parameters:
        - word_set: Set of valid words from greek alphabet
        """
        match self.mode:
            case 'min':
                return self.minLetters(word_set)
            case 'max':
                return self.maxLetters(word_set)
            case 'smart':
                return self.smart(word_set)
        
    





game = Game()
game.loadWords()
print(game.wordsSet)

