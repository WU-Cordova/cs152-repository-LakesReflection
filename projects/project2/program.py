from datastructures.bag import Bag
import random
import time
import os
def ansi(*args):
    PrintBuf=""
    for i in args:
        PrintBuf+="\033[" + i
    print(PrintBuf,sep="",end="")
NUMROWS= os.get_terminal_size().lines
NUMCOLS = os.get_terminal_size().columns
def main():
    #genuinely I wouldn't use a bag structure here?
    # theres no good way to get weights
    #
    class Game():
        class Hand():
            def __init__(self,ActGame) -> None: #init would be passed balance if tracking that
                self.cards =None
                self.val = 0
                self.game = ActGame
                self.line=0
                self.fAce =False
            def deal(self):
                pass
            def turn(self):
                pass
            def hit(self):
                self.cards += self.game.Draw(1)
                self.val += self.CardVal(self.cards[-1][0])
                ansi(str(self.line+1)+";" + str(2*len(self.cards) -1)+"H")
                ansi(("0;"+str(self.cards[-1][1]+31)+"m "+
                     chr(0x1F0A1 + self.cards[-1][0] 
                     +(16*self.cards[-1][1]))+" "))
                ansi(str(self.line+2)+";3H")
                ansi("2K" + str(self.val))




            def CardVal(self,inCard):
                if inCard == 0:
                    self.fAce = True
                    return inCard + 1
                elif inCard >9:
                    return 10
                else:
                    return inCard +1
        class Dealer(Hand):
            def __init__(self, ActGame) -> None:
                super().__init__(ActGame)
                self.line=1
            def deal(self):
                ansi("1;1H Dealer")
                self.cards = self.game.Draw(2)
                self.val = self.CardVal(self.cards[1][0])
                ansi("2;2H", "39;48m"+chr(0x1F0A0),
                     ( "0;"+str(self.cards[1][1]+31)+"m "+
                     chr(0x1F0A1 + self.cards[1][0] 
                     +(16*self.cards[1][1]))+" "))
                ansi("39;49m", "1B", "3D" + str(self.val))
                self.val += self.CardVal(self.cards[0][0])
            def turn(self):
                ansi(str(self.line +1)+";0H")
                ansi(
                    ( "39;"+str(self.cards[0][1]+31)+"m "+
                     chr(0x1F0A1 + self.cards[0][0] 
                     +(16*self.cards[0][1]))+" ")
                     )
                while self.val <16:
                    self.hit()
        class Player(Hand):
            def __init__(self, ActGame) -> None:
                super().__init__(ActGame)
                self.line = 6
            def deal(self):
                ansi(str(NUMROWS-2)+";0H h: hit s:stay")
                ansi("6;1HYou") ##lines 3 8 for values 
                self.cards = self.game.Draw(2)
                ansi("7;1H")
                self.val = 0
                for i in self.cards:
                    ansi(("0;"+str(i[1]+31)+"m"+ chr(0x1F0A1 + i[0] +(16*i[1]))+" "))
                    self.val += (self.CardVal(i[0]))
                ansi("39;49m", "1B", "3D" + str(self.val))

            def turn(self):
                while self.val < 21:
                    ansi(str(NUMROWS-1) +";1H", "39;49M")
                    choice =input().lower() #t split d doubledown
                    ansi("2K","1G")
                    match choice:
                        case "s" | "stay":
                            return
                        case "h" | "hit":
                            self.hit()
                        case _:
                            pass












        def __init__(self,deck) -> None:
            ansi("3J", #clears scnreen
             "?1049h", #alt screen enable
             "?25l", #hides cursor
             "1;1H") # top of screen
            self.num_decks = random.randint(1,4)
            multideck = []
            for _ in range(2*self.num_decks):
                multideck += deck
            self.activeDeck=Bag(*multideck)
            self.dealer=self.Dealer(self)
            self.player=self.Player(self)
            self.Round()
            self.Gameover()


        def Gameover(self):
            if self.player.fAce ==True: #this doesnt work with multi aces
                if self.player.val +10 > 21 or self.player.val > self.dealer.val:
                    pass
                elif self.player.val +10 > self.dealer.val:
                    self.player.val +=10

            if ( 22>self.dealer.val >= self.player.val or
                    self.player.val > 21):
                results=("Dealer Wins")
            elif( self.player.val == self.dealer.val ):
                results = ("Tie")
            else:
                results = ("Player Wins")
            ansi("39;49m")
            ansi(f"{NUMROWS//2};0H")
            choice = input(f"D{self.dealer.val}-P{self.player.val} \n {results}\n play again (y/n)").lower()
            ansi("3J")
            match choice:
                case "y" | "yes":
                    self.Round()
                    self.Gameover() #ooo <- Bad recusrsion
                case _:
                    pass

        def Round(self):
            self.player.deal()
            self.dealer.deal() 
            self.player.turn()
            self.dealer.turn()

            # this sucks as a way to do to this but is nesscary 
            # to make the bag remotely work randomly

        def Draw(self, numcards):
            cur_count=0
            def CardCheck(bundle):
                draw,top = bundle
                nonlocal cur_count
                if not isinstance(draw, int):
                    return draw
                else:
                    draw = draw-cur_count
                    if draw < 0:
                        cur_count -= 1
                        return top
                    
                    else: 
                        return draw
            drawn =[]
            for i in range(numcards):
                drawn.append(random.randint(0,(len(self.activeDeck))))
            for i in self.activeDeck.distinct_items():
                cur_count= self.activeDeck.count(i)
                drawn = list(map(CardCheck, [(x,i) for x in drawn]))

            redraw=0
            for n in drawn:
                if n in self.activeDeck:
                    self.activeDeck.remove(n)
                else:
                    drawn.remove(n)
                    redraw +=1
            if redraw:
                drawn += self.Draw(redraw)
            return drawn











    single_deck = []
    for face in range(14):
        for suit in range(4):
            single_deck.append((face,suit))
    CurGame = Game(single_deck)




if __name__ =='__main__':
        main()
