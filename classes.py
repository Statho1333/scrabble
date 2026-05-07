import itertools as it
import os
import json
import random
import sys
from collections import Counter
from abc import ABC, abstractmethod

def documentation():
    """
    -Κλάσεις: Game, SakClass, Player, Human, Computer
    -Κληρονομικότητα: Player παράγωγη κλάση της ABC (για να εφαρμόσω abstract method την play, όπως κάναμε στην java)
                      Computer, Human παράγωγες κλάσεις της Player.
    -Επέκταση Μεθόδων: έχω επεκτείνει την play, δημιουργόντας πολυμορφισμό στον τρόπο που καλείται από τις Human και Computer.
    -Υπερφόρτωση τελεστών: Έχω εφαρμόσει 2 υπερφορτώσεις τελεστών.
                            1. Στην build-in συνάρτηση __len__ στην κλάση Player ώστε όταν καλείς len(self.player) να σου επιστρέφει το μήκος του χεριού παίκτη. Η ίδια υπερφόρτωση έγινε και για την SakClass που σου επιστρέφει πόσα γράμματα έμειναν στο σακούλι. Αντί για len(self.sak.sak) πλέον με len(self.sak) έχεις το ίδιο αποτέλεσμα.
                            2. Στην build-in συνάρτηση __sub__ πάλι στην κλάση Player, με σκοπό να μπορεί κάποιος έυκολα να αφαιρεί από το χέρι του παίκτη, τα γράμματα που χρησιμοποίησε για να παίξει μία λέξη. Δλδ μπορεί κάποιος πλέον εύκολα να πει self.human-=word.
    -Decorators: 1. staticmethod η calculateScore όπου υπολογίζει τους βαθμούς μία λέξης στην κλάση Player
                 2. abstract method η play μέσα στην κλάση Player
    -Δομή λέξεων: Επιλέχτηκε set για να τηρούνται οι απαιτήσεις αναζήτησης Ο(1).
    -Αλγόριθμος Πολιτικής Παιχνιδιού: Αλγόριθμος 1 (Min - Max - Smart)
    -Πρότυπο Mediator: Η κλάση Game γνωρίζει όλα τα αντικείμενα και διαχειρίζεται την επικοινωνία μεταξύ τους. Οι παίκτες δεν επικοινωνούν απευθείας μεταξύ τους. Επίσης η Game διαχειρίζεται το SakClass και μοιράζει αυτή γράμματα στους παίκτες. Ελέγχει την εγκυρότητα των λέξεων και τους προσθέτει/αφαιρεί πόντους. Τέλος ελέγχει πότε τελειώνει το παιχνίδι, και είναι υπεύθυνη για την ανακοίνωση των αποτελεσμάτων.
    """


class Game():
    """
    Mediator class that handles all the communication between the Players objects and the SakClass object.
    """
    def __init__(self):
        self.sak = SakClass()
        self.wordsSet = self.loadWords()
        self.human = None
        self.computer = None
        self.onGoingGame = False

    def __repr__(self):
        """Prints basic inforamtion about the game, if it is set."""
        print(f'Game Scrabble')
        if self.sak is not None:
            print(f'Στο σακουλάκι απομένουν {len(self.sak)} γράμματα')
        if self.human is not None:
            print(f'Παίκτης: {self.human.name} | Σκορ: {self.human.score}')
        else:
            print(f'Παίκτης: Δεν έχει οριστεί')
    
        if self.computer is not None:
            print(f'Αντίπαλος: {self.computer.name} | Δυσκολία: {self.computer.mode} | Σκορ: {self.computer.score}')
        else:
            print(f'Αντίπαλος: Δεν έχει οριστεί')

    def showStartingInterface(self):
        """
        Shows the starting interface of the project guide. Directs the user to the next menu, according to his choice.
        """
        choices = ('1','2','3','q')

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
        """
        Refers to option 1: Σκορ in project guide. Shows the scores of the players
        """
        if self.human is None:
            print(f'Δεν υπάρχει ακόμα παιχνίδι!')
            return
        print(f'{self.human.name} score is: {self.human.getScore()}')
        if self.computer is not None:
            print(f'{self.computer.name} score is: {self.computer.getScore()}')
        else:
            print(f'Δεν υπάρχει αντίπαλος ακόμα')

    def setup(self):
        """
        Refers to option 2: in project guide.
        Basic configuration for the game to run.
        Sets players name and computers name. From the name of the computer derives the gaming algorithm which is equal to difficulty.
        Reprompts user for choices that are not valid.
        There is an option to load previus game.
        """
        choices = ('1','2','3','b')

        if input(f'Θέλεις να φορτώσεις αποθηκευμένο παιχνίδι; (Υ/Ν) ').upper() == 'Y':
            if not self.loadGame():
                return
            self.run()
        
        else:

            humanName = input(f'Το όνομά σου είναι: ')
            self.human = Human(humanName)

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
                        case '2':
                            computerName = 'R2D2'
                        case '3':
                            computerName = 'BB-8'

                    
                    self.computer = Computer(computerName)
                    self.sak = SakClass()
                    self.human.hand = self.sak.getLetters(7)
                    self.computer.hand = self.sak.getLetters(7)
                    self.human.score = 0
                    self.computer.score = 0
                    return


    def loadWords(self) -> set:
        """
        Loads the 'greek7.txt' file.
        
        Returns:
        - a set of words if file found, empty set otherwise
        """
        try:
            with open('greek7.txt', 'r', encoding='utf-8') as f:
                return {line.strip() for line in f}
        except FileNotFoundError:
            print('Το αρχείο δεν βρέθηκε')
            return set()
        
    def refillHand(self,player : Player):
        """
        Refills the hand of a Player. Checks if it can change all 7 letters from the hand of the player. If less than 7 letters are in the sak, reffils only those.

        Parameters:
        - player: an Instance of Human or Computer that calls the function

        Return:
        A new hand for the player 
        """
        needed = min(7-len(player), len(self.sak))
        player.hand+= self.sak.getLetters(needed)

    def run(self):
        """
        Refers to option 3 in project guide.
        Controls the flow of the game between the human and the computer Player.
        Automatically checks if the game has come to a dead-end and calls announces the winner.
        """
        if self.human is None:
            print(f'Δεν έχεις ρυθμίσει ακόμα παίκτη')
            return

        if self.computer is None:
            self.computer = Computer('C3PO')

        if len(self.human)==0:
            self.human.hand = self.sak.getLetters(7)
        if len(self.computer) == 0:
            self.computer.hand = self.sak.getLetters(7)

        while True:
            humanCanPlay = False
            computerCanPlay = False
            humanChanged = False

            #HUMAN ACTIONS
            while True:
                self.human.__repr__()
                print(f'Αν θέλεις να αλλάξεις τα γράμματά σου, πληκτρολόγησε "P"')
                print(f'Αν θέλεις να παραιτηθείς πληκτρολόγησε "Q"')
                print(f'Αν θέλεις να παίξεις, απλά πληκτρολόγησε την λέξη σου')
                word = input('ΛΕΞΗ Ή ΕΠΙΛΟΓΉ: ').upper()
                response, option = self.human.play(word,self.wordsSet)

                if not response and option == 'Change':
                    humanChanged = True
                    if len(self.sak) == 0:
                        print(f'Δεν υπάρχουν άλλα γράμματα για αλλαγή, χάνεις την σειρά σου')
                    else:
                        self.sak.putBackLetters(self.human.hand)
                        self.human.hand = []
                        self.refillHand(self.human)
                    break
                elif not response and option == 'End':
                    self.tapOut()
                    return
                elif response and option == 'Valid':
                    humanCanPlay = True
                    score = self.human.calculateScore(word)
                    self.human.addScore(score)
                    self.human = self.human - word
                    self.refillHand(self.human)
                    print(f'Πόντοι λέξης: {score}')
                    self.human.__repr__()
                    break
                else:
                    print(f'Δεν υπάρχει η λέξη που πληκτρολόγησες, προσπάθησε ξανά!')

            #check after human
            if len(self.sak) <=1 and len(self.human) <=1:
                self.end(gameOver=True)

            #Computer actions
            self.computer.__repr__()
            computerWord, computerScore = self.computer.play(self.wordsSet)
            if computerWord is None:
                if len(self.sak) == 0:
                    self.end(gameOver=True)
                else:
                    print(f'{self.computer.name} δεν βρήκε λέξη, αλλάζει γράμματα!')
                    self.sak.putBackLetters(self.computer.hand)
                    self.computer.hand = []
                    self.refillHand(self.computer)
            else:
                computerCanPlay = True
                self.computer.addScore(computerScore)
                self.computer = self.computer - computerWord
                self.refillHand(self.computer)
                print(f'O {self.computer.name} έπεξε την λέξη: {computerWord}!')
                print(f'Πόντοι λέξης: {computerScore}')
                self.computer.__repr__()

            if self.isGameOver(humanCanPlay, computerCanPlay, humanChanged):
                self.end(gameOver=True)


    def isGameOver(self, humanCanPlay: bool, computerCanPlay: bool, humanChanged: bool) -> bool:
        """
        Checks when the criteria is met to end game automatically.

        Parameter:
        - humanCanPlay: bool.
        - computerCanPlay: bool
        - humanChanged: bool

        Returns:
        - True, if sak is empty and hand of human or computer is empty or when human cant and computer cant play and human couldnt change hand.
        - False, otherwise
        """
        #print(f'DEBUG: humanCanPlay={humanCanPlay}, computerCanPlay={computerCanPlay}, humanChanged={humanChanged}')
        #print(f'DEBUG: sak={len(self.sak)}, human hand={len(self.human)}, computer hand={len(self.computer)}')
        if not humanCanPlay and not computerCanPlay and not humanChanged:
            return True
        if len(self.sak) == 0 and len(self.human) == 0:
            return True
        if len(self.sak) == 0 and len(self.computer) == 0:
            return True
        return False

    def printEndResults(self):
        """
        Prints info for the winner
        """
        print(f'****************************************************')
        print(f'ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ')
        print(f'Τελικο σκορ')
        print(f'{self.human.name}: {self.human.score} πόντοι')
        print(f'{self.computer.name}: {self.computer.score} πόντοι')

        if self.human.score > self.computer.score:
            print(f'Νικητής ο {self.human.name}!!! Συγχαρητήρια!!!')
        elif self.human.score<self.computer.score:
            print(f'Κρίμα σε νίκησε ο {self.computer.name}. Προσπάθησε ξανά!!')
        else:
            print(f'Ισοπαλία!!!!!!!!')

    def end(self, gameOver=False):
        """
        Ends game. 

        Parameters:
        - gameOver: bool. Defines if game was ended normally, or the user exited the game.
        If game ended normally, prints the winner, and removes old save, otherwise saves game and exits game.
        """
        if gameOver:
            self.printEndResults()
            if os.path.exists('save.json'):
                os.remove('save.json')
        else:
            self.saveGame()

        print(f'Τα λέμε την επόμενη φορά!')
        sys.exit()


    def saveGame(self):
        """
        Saves game status in a json file
        """
        data = {
            'sak': self.sak.sak,
            'humanName': self.human.name,
            'humanHand': self.human.hand,
            'humanScore': self.human.score,
            'computerName': self.computer.name,
            'computerHand': self.computer.hand,
            'computerScore': self.computer.score,
            'computerMode': self.computer.mode
        }
        with open('save.json', 'w', encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False)

    def loadGame(self) -> bool:
        """
        Loads game from josn file 'save.json'
        
        Returns:
        - True: if load was successful
        - False: if file doesnt exist, or error happened in loading precedure
        """
        if not os.path.exists('save.json'):
            print(f'Δεν υπάρχει το αρχείο "save.json" για να συνεχίσετε το παιχνίδι σας.')
            print(f'Υποχρεωτικά ξεκινήστε καινούργιο παιχνίδι')
            return False
        
        try:
            with open('save.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sak.sak = data['sak']


                self.human = Human(data['humanName'])
                self.human.hand = data['humanHand']
                self.human.score = data['humanScore']

                self.computer = Computer(data['computerName'])
                self.computer.hand = data['computerHand']
                self.computer.score = data['computerScore']
                self.computer.mode = data['computerMode']
            return True
        except:
            print(f'Σφάλμα κατά την φόρτωση του αρχείου')
            return False
        
    def tapOut(self):
        """
        Defines what happen when the user surrender.
        Sets the hand of human and computer to [], and their scores to 0.
        Remakes a new Sak instance, with new letters.
        Removes the older saved game, if it existed
        """
        print(f'Κρίμα! Έχασες γιατί παραιτήθηκες.')
        self.human.score = 0
        self.computer.score = 0
        self.human.hand = []
        self.computer.hand = []
        self.sak = SakClass()
        if os.path.exists('save.json'):
            os.remove('save.json')
        return


    


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
        self.sak = self.randomizeSak()

    #takes as input a random dictionary of letters, flattens it and shuffles it
    def randomizeSak(self) -> list:
        """
        Function that flattens the letters dictionary, converting it to a string, and shuffles it,cdepending on the occurences of each letter

        Attributes:
        - letters: the class attribute lets dictionary

        Returns:
        sak: a shuffled list of letters
        """
        sak = [letter for letter, (count, points) in SakClass.lets.items() for _ in range(count)]
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


class Player(ABC):
    """
    Basic class of players, from which derives Human and Computer
    Cant create directly Player instance, only Human or Computer
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

    @staticmethod
    def calculateScore(word: str) -> int:
        """
        Calculates the points of a word
        Static Method.

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
    def play(self,word: str, word_set: set):
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
        
    







