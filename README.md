# An Autonomous Pokerbot
### In January of 2021, I participated in the MIT Pokerbots Competition, a poker tournament in which Teams have one month to program a completely autonomous pokerbot which competes against other bots.

> Poker is a game of incomplete information and uncertainty. It is a prime application of the game theory concepts and decision making skills essential to trading. While traders make risk decisions based on the limited information they get from the markets, poker players make decisions based on hidden information as well, taking into account factors such as expected value and probability distributions.
> 
> To win, competitors must learn and apply concepts in mathematics, computer science, and economics.
> 
> The reigning Pokerbots champion is a product of excellent programming ability and strategic quantitative thinking skills!

I have learned that similar to TRADING, game theory concepts and decision making skills are essential in Poker. While traders make risk decisions based on the limited information they get from the markets, poker players make decisions based on hidden information as well

To win, competitors must learn and apply concepts in mathematics (expected value and probability distributions), computer science, and economics.

A pokerbot champion is a product of excellent programming ability and strategic quantitative thinking skills!

### STRATEGIES AND IMPLEMENTATION: 
* For fast runtime, my bot played millions of simulated pokergames and precomputed poker-hand strengths before the tournament.
* To automate decision making, I applied risk-reward calculations , and for the best outcome, I followed a tight-aggressive (bet big on strong hands) playing style. 
* I also adds randomization so my strategies are not predicted and exploited by other bots.
### In the end, I alone built a bot (using Python), that could easily beat Difficult-level Staff bot.
### My bot also ranked above average pokerbots built by teams of 4 MIT students . It has a winrate of > 50%, and above average ELO rating.

![win loss](winloss.png?raw=true)


## USAGE:

- The bot requires the following Python3 modules: ??? cython ??? eval7

- Go to the directory of the engine and run the command ???$ python3 engine.py

- The engine will run one game according to the parameters in ???config.py and will save the results in several files outlined below:

  + A.txt Text log of all output (print/error) from the bot of the player named ???A???.

  + B.txt Text log of all output (print/error) from the bot of the player named ???B???. 

  + gamelog.txt Text log for the game named ???gamelog???. This will be the most useful file for determining what happened in the game.

- Parameters: The parameters to the game engine are controlled via the configuration file ???config.py in the same directory as the engine file ???engine.py???. 


## Final Bot (python_precomputed_parameterized_v6): Demonstration

In config.py, set Hero bot to be v6 (tight-agressive playing style i.e. big bet on strong hands, plus randomness for unpredictability, and pre-computed hand strength for faster speed),  V.S. Evil bot v3 (which implemented pot odds i.e. risk-reward calculations. V3 could beat Easy-level MIT Staff bot):

![image](https://user-images.githubusercontent.com/58123635/121759714-2155c700-caf5-11eb-9cb2-02bb3390e35e.png)

And the results:
![image](https://user-images.githubusercontent.com/58123635/121759887-eacc7c00-caf5-11eb-8203-c5db8835d92b.png)


