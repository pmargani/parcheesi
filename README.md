# parcheesi

A simulator for determining optimal parcheesi play

## Motivation

For a game with such incredibly simple rules, I find Parcheesi to be incredibly entertaining.  However, one thing that has been noticed is how long the games can take.

Why is this?  It must have something to do with how we are playing?  And if different strategies for playing lead to longer games, can they also really make a difference in terms of who wins?

## The Game

Parcheesi is a brand-name American adaptation of the Indian cross and circle board game Pachisi:

https://en.wikipedia.org/wiki/Parcheesi

<img src="images/Parcheesi-board.jpg" alt="Parcheesi-board.jpg" width="500">

Parcheesi is typically played with two dice, four pieces per player and a gameboard with a track around the outside, four corner spaces and four home paths leading to a central end space. The most popular Parcheesi boards in America have 68 spaces around the edge of the board, 12 of which are darkened safe spaces. Each corner of the board contains one player's nest, or starting area. 

### Setup

   * Each player positions their four single colored pieces in their respective starting nest.
   * Each player rolls a single die to determine player order. The player with the lowest roll goes first.
   * The order of players' turns moves to the next player on the current player's left.
   * Pieces move from the nest to the colored starting space to the left of the nest, per rules in the following section.


### Rules

Like a lot of games, I have been playing Parcheesi with silightly modified rules.  Here's the gist of how I play it:

A player rolls the dice and must use the topmost facing die pip values shown to move their pieces around the board in one of the following ways:

   * Only pieces not in the nest may move forward on the board.
   * Pieces may only leave the nest with a roll of a five on a single die or the sum of the dice. A double five can be used to move two pieces from the nest simultaneously.
   * In the case of a non-doubles roll, a player may move one or two pieces, either one piece by each of the numbers on the two dice or one piece by the total. If no move is possible, the turn is forfeited.
   * When moving a single piece the total of two dice the turn is taken in increments, allowing pieces to be captured along the way. For example, if a double two is rolled and an opponent's piece lies on a cream space two spaces in front of the piece you wish to move the full four, you would move the piece two, and then two again, allowing the opponent's piece to be captured.
   * All die rolls must be taken and may not be voluntarily forfeited by a player.
   * If a player cannot use both dice, the player must use one of the dice, if possible. If either can be used, the player must use the largest die.
   * When the player rolls doubles, the player rolls again after moving, provided all of the doubles roll was used. If the player is unable to use all of the roll, the player doesn't get another roll.
   * When a piece ends its move on the same space as an opponent's piece, the opponent's piece is sent back to its nest.
   * A piece may not be placed on a safe space (generally colored light blue) if it is occupied by an opponent's piece. The exception is the safe space used when a piece leaves its nest — a single piece occupying such a safe space is sent back to its nest when an opponent's piece leaves the nest and occupies the space.
   * A blockade is formed when two pieces occupy the same space. No piece of any player may move through a blockade, including pieces of the blockade owner. 

Winning the game:
   * Moving all four pieces to the home position wins the game.[1]
   * Pieces may only be moved to the home position with an exact application of the total roll, the value on a single die,   
  
### Strategies

One can see that sometimes there's not a lot of choices for the player to make: a lot is determined by the die roll and contraints on the board.

But when there are choices, what are the best options that would lead to winning?  And do some of these lead to longer games?  

A lot of these choices can be thought of in terms of offensive, or defensive moves.  Here's some examples of choices that a player can make:


   * when the opportunity arises to send back an oppenents piece to their nest, is it worth the risk of exposing this piece to attack itself?  Or advancing another piece?
   * does maintaining a blockade to keep opponent pieces from advancing worth the fact that these pieces in the blockade themselves are not advancing?  Even when there are other pieces that do get advanced?
   * when rolling a five and there are pieces in the nest, should the priority be to get these pieces out, over possibly securing or advancing other pieces?

## Installation and Running

The usual steps can be done for building the needed virtual environment:
   * python -m venv $VIRTUAL_ENV
   * source $VIRTUAL_ENV
   * cd parcheesi
   * pip install --upgrade pip
   * pip install -r requirements.txt

Running things:
   * tests: pytest test_*
   * to run simulations given parameters in main.py: python main.py

      
## Design

We take a standard Object Oriented Programming approach, with classes representing pieces and players.  The board itself is represented as a list of numbers representing positions on the board.  A pygame interface is being implemented to visualize the game play and enable human vs. computer games, but is a work in progress.

Currently the game rules are mostly implemented in functions in a game module.  The game and the module should become classes themselves it seems.

In regards to strategies, there is only one current very simple strategy:
   * always get a piece out of the nest when possible
   * simply take the first legal move available to the piece that is furthest ahead

Obviously there is no regard for offensive or defensive moves yet.

## Current Results

Currently the only thing we can do is play a full game with randomized dice rolls and the above mentioned strategy.  But we can collect metrics such as how many turns the game takes, how many times each player is blocked or sent back to the nest, etc.

Here are some results from running the game 10,000 times using the one above mentioned, simple strategy:

<img src="images/winTurns.png" alt="winTurns.png" width="500">

Above we have the number of turns (for all players) before the first player wins.  We can see that the mean number of turns before the game has a winner (recall that players can decide to keep playing to see who gets second, etc) is 244.  

If each turn takes 15 seconds (this would be an extermely efficient game), then 244 turns would take about an hour.  This is *much* faster then the games I have experience playing, that can take up to *three* hours.  This may simply be a direct consequence of sending other players back to home, and blocking them.  We'll see about this once we start running the game with different strategies.

<img src="images/turns.png" alt="turns.png" width="500">

Above we see how many turns it takes to get *all* the players' pieces into home.  Obviously this takes a little longer then just for the first player to get all their pieces home.

<img src="images/blocks.png" alt="blocks.png" width="500">

Above we see how many times a player cannot move a piece.  Note that this could be any number of factors:  all pieces are in the nest and a 5 was not rolled, or all pieces out of the nest are behind another player's blockade.  It would be interesting to track these different circumstances separately.

<img src="images/deaths.png" alt="deaths.png" width="500">
<img src="images/kills.png" alt="kills.png" width="500">

Above we see how many times in a given game a piece is sent back to home ('death') or a piece sends another piece home ('kill').  The fact that these plots are identical is a very good sanity check.  I am surprised at how many times pieces are sent back when using a strategy that is not trying to do this: it's simply statistics.

<img src="images/doubles.png" alt="doubles.png" width="500">

Speaking of statistics, above shows the number of times doubles were rolled.  It would be good to check that this makes statistical sense, since the rolling of the dice isn't affected by anything going on on the board.

<img src="images/doubleDeaths.png" alt="doubleDeaths.png" width="500">

In the above plot we have more results that can be confirmed statiscally: what are the odds of rolling three doubles in a row when the dice are rolled for about 244 turns?

What's interesting is that the mean is 1.36.  So it's not unreasonable that this type of thing should happen once or twice per game.  But why does it always happen to me?






