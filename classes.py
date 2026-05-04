import itertools as it
import json
import random
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
        


    def run(self):     
        if self.computer is None:
            self.computer = Computer('C3PO', 'min')

        while True:
            pass


    def end(self):
        pass


    


class SakClass():

    lets = {'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],
        'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],
        'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],
        'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],
        'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3]
        }
    
    def __init__(self):
        self.sak = self.randomizeSak(SakClass.lets)

    #takes as input a random dictionary of letters, flattens it and shuffles it
    def randomizeSak(self, letters: dict):
        sak = [letter for letter, (count, points) in letters.items() for _ in range(count)]
        random.shuffle(sak)
        return sak

    #removes n letters from sak
    def getLetters(self, n: int) -> list:
        letters = self.sak[:n]
        self.sak = self.sak[n:]
        return letters
    
    #places back the letters, expecting a list to be given
    def putBackLetters(self,letters: list[str]):
        self.sak.extend(letters)
        random.shuffle(self.sak)

    #returns the len of the sak
    def __len__(self) -> int:
        return len(self.sak)


class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def __repr__(self):
        pass

    def getScore(self):
        return self.score
    
    def addScore(self,points):
        self.score+=points

    def calculateScore(self,word: str) -> int:
        return sum(SakClass.lets.get(letter)[1] for letter in word)
    
    @abstractmethod
    def play(self,sak,word_set):
        pass


class Human(Player):
    def __init__(self,name):
        super().__init__(name)

    def play():
        pass

class Computer(Player):
    def __init__(self, name='C3PO'):
        super().__init__(name)
        self.mode = self.pickMode(self.name)

    def pickMode(self, name: str) -> str:
        match name:
            case 'C3PO':
                return 'min'
            case 'R2D2':
                return 'max'
            case 'BB-8':
                return 'smart'
            
    def minLetters(self,validWords: set) -> tuple:
        for length in range(2,len(self.hand)+1):
            for perm in it.permutations(self.hand,length):
                word = ''.join(perm)
                if word in validWords:
                    return word, self.calculateScore(word)
        return None, 0

    def maxLetters(self,validWords: set) -> tuple:
        for length in range(len(self.hand), 1, -1):
            for perm in it.permutations(self.hand, length):
                word = ''.join(perm)
                if word in validWords:
                    return word, self.calculateScore(word)
        return None, 0

    def smart(self,validWords: set) -> tuple:
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
    





game = Game()
game.loadWords()
print(game.wordsSet)

