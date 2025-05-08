First I did use wikipedia for this some, I have qouted the section which heavily informed my desgin
At the bottom of this doc.

NOTE - I used ansi escape charachters alot. It is possible other terminal emulators implment less of these then mine does. I stuck to vt100 and some xterm extensions. The terminal I use is kitty





The data flow is kinda weird so heres an explanation and an illustration.

Lets say you have row A,B,and C
A= x, y, z
B= e, f, g
C= u, v, w

Each Row must first pass through the Down buffer before its in the up Buffer.
The Down Buffer iteraviely sums the neghbors and the corsepending vaule to its next iteration.
Beta stage of Down Buf (Alpha is talked about later)
So first cycle of the DownBuffer:
    We start with x as first element.
    We take the sum of x+y and write that to Downbuffer[0]
    We then write x to DownBuffer[1]
Second Cycle:
ay is focused element.
We agin sum ay and its right neighbor
y+z, but we add that to DownBuffer[1]
Since we wrote x in that spot last cycle,
this is equivalent to x + y + z
again write ay to DownBuf[2]
Last cycle
DownBuf[2] = az+0(right -neghibor)

The important thing to note is that DownBuffer
now contains the sum of itself and its neghbiors, but only within its row

UpBuf Is the the sum of a rows downBuf and the row before its downbuf
So lets say UpBuf currently corrseponds to Row B, and DownBuf Row C
Upbuf[0] = (x+y)+(e+f)
DownBuf[0] =(u+v)
I hope you can see that by adding DownBuf to UpBuf you get the sum of e and its neighbors.
If all the vaules were just boolean 0 for dead, 1 for alive
As the Wikipedia article points out this sum tells the state that the cell e should be in.

Okay but how does Upbuf come to contain the sum of the prior two?
Its actually super similar to how the first stage of DownBufs calcutions worked.
If we just used DownBuf Beta Stage, when we iter to a new row all the info stored it wouldn't be super helpful
And also notice that once we find the state of cell that information in UpBuf becomes pointless and redudant as we
write to array.
This lets us store extra information in DownBuf before we overwrite with calcuation of neghibors.
But to Free a cell in UpBuf we do need to do the calcution, which would overwrite ourdata.
So instead we store the Sum of Row Neighbors in tempoary variable, call it LocSum.

So we Add that to a cell in BufUp[n] and push that to the array.
Then we store Locsum in BufUp.
The extra values we've been storing in DownBuff are the prior rows (LocalSum), turns out it actually is useful
We then *add* our LocSum To Bufdown[n] - which gives the sum of The current Row and the prior one
So when iterate to the next row, this will be the sum of the prior two.
Finally we Swap BufUp and BufDown, 
so that when start the next iteration BufUp holds The Sum of the prior two Rows and BufDown Holds the prior rows Locsums.
(Also Loc Sum not BufDown[n+1] holds the vaule of CurrentRow[n], cause again its holding the result of calcutations)

Illustration:
⟰ =BufUp
⟱ = BufDown


Starting Values:
A= x, y, z
B= e, f, g
C= u, v, w
⟰ = [((x+y)+(e+f)), ((x+y+z)+(e+f+g)), ((y+z)+(f+g))]
⟱ = [(e+f), (e+f+g), (f+g)]
UpRow=B
DownRow=C
LocSum=0

Step 1:

LocSum = Locsum + C[0]+C[1] -> 0+u+v

BufUp[0] = BufUp[0] +LocSum ->  ((x+y) +(e+f)) + (u+v)
Write dervied bool from BufUp[0] to Array
BufUp[0]= LocSum -> (u+v)
BufDown[0] = BufDown[0]+LocSum -> (e+f)+(u+v)
LocSum = C[0] -> u

Buffer states end step 1:
⟰  == [(u+v), ((x+y+z)+(e+f+g)), ((y+z)+(f+g))]
⟱  == [((e+f)+(u+v)), (e+f+g), (f+g) ]


Step 2:

LocSum = Locsum + C[1]+C[2] -> u + v + w
BufUp[1] = BufUp[1] +LocSum ->  ((x+y+z) +(e+f+g)) + (u+v+w)
Write dervied bool from BufUp[1] to Array
BufUp[1]= LocSum -> (u+v+w)
BufDown[1] = BufDown[1]+LocSum -> (e+f+g)+(u+v+w)
LocSum = C[1] -> v


Buffer states end step 2:
⟰  == [(u+v), (u+v+w), ((y+z)+(f+g))]
⟱  == [((e+f)+(u+v)), ((e+f+g)+(u+v+w)), (f+g) ]


Step 3:
LocSum = Locsum + C[2]+C[3]  -> v + w + 0
BufUp[2] = BufUp[2] +LocSum ->  ((y+z) +(f+g)) + (v+w)
Write dervied bool from BufUp[2] to Array
BufUp[2]= LocSum -> (v+w)
BufDown[2] = BufDown[2]+LocSum -> (f+g)+(v+w)
LocSum = C[2] -> w

Buffer states end step 3:
⟰  == [(u+v), (u+v+w), ((y+z)+(f+g)]
⟱  == [((e+f)+(u+v)), ((e+f+g)+(u+v+w)), ((f+g)+(v+w)) ]















Wikipedia Lines thar were super helpful:

"To avoid decisions and branches in the counting loop, the rules can be rearranged from an egocentric approach of the inner field regarding its neighbours to a scientific observer's viewpoint: if the sum of all nine fields in a given neighbourhood is three, the inner field state for the next generation will be life; if the all-field sum is four, the inner field retains its current state; and every other sum sets the inner field to death.

To save memory, the storage can be reduced to one array plus two line buffers. One line buffer is used to calculate the successor state for a line, then the second line buffer is used to calculate the successor state for the next line. The first buffer is then written to its line and freed to hold the successor state for the third line. If a toroidal array is used, a third buffer is needed so that the original state of the first line in the array can be saved until the last line is computed.

In principle, the Game of Life field is infinite, but computers have finite memory. This leads to problems when the active area encroaches on the border of the array. Programmers have used several strategies to address these problems. The simplest strategy is to assume that every cell outside the array is dead. This is easy to program but leads to inaccurate results when the active area crosses the boundary. A more sophisticated trick is to consider the left and right edges of the field to be stitched together, and the top and bottom edges also, yielding a toroidal array. The result is that active areas that move across a field edge reappear at the opposite edge. "
