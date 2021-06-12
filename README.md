# An Autonomous Pokerbot
### In January of 2021, I participated in the MIT Pokerbots Competition.

### In the end, I alone built a completely autonomous pokerbot (using Python), that could easily beat Difficult-level MIT Staff bot. 

### My bot also ranked above the average pokerbots built by teams of 1-3 MIT students (with winrate > 50%, and above average ELO rating).

![win loss](winloss.png?raw=true)


## USAGE:

- The bot requires the following Python3 modules: ● cython ● eval7

- Go to the directory of the engine and run the command ​$ python3 engine.py

- The engine will run one game according to the parameters in ​config.py and will save the results in several files outlined below:

  + A.txt Text log of all output (print/error) from the bot of the player named ​A​.

  + B.txt Text log of all output (print/error) from the bot of the player named ​B​. 

  + gamelog.txt Text log for the game named ​gamelog​. This will be the most useful file for determining what happened in the game.

- Parameters: The parameters to the game engine are controlled via the configuration file ​config.py in the same directory as the engine file ​engine.py​. 


## Final Bot (python_precomputed_parameterized_v6): Demonstration

In config.py, set Hero bot to be v6 (tight-agressive playing style i.e. big bet on strong hands, plus randomness for unpredictability, and pre-computed hand strength for faster speed),  V.S. Evil bot v3 (which implemented pot odds i.e. risk-reward calculations. V3 could beat Easy-level MIT Staff bot):

![image](https://user-images.githubusercontent.com/58123635/121759714-2155c700-caf5-11eb-9cb2-02bb3390e35e.png)

And the results:
![image](https://user-images.githubusercontent.com/58123635/121759887-eacc7c00-caf5-11eb-8203-c5db8835d92b.png)


