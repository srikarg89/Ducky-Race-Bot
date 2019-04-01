# Ducky-Race-Bot
Roast your friends in [Ducky Race](https://www.arcademics.com/games/ducky-race) with this speedster bot.
## Dependencies

- [OpenCV](https://opencv.org/)
- [Pyautogui](https://pyautogui.readthedocs.io/en/latest/)

## Information
The code contains two main sections: Interfacing with the game and classification.
The program finds the lcoations of the text boxes and takes pictures of them.
Using contour matching, the code classifies each of the numbers, finds the correct answer, and clicks on it.

Rinse and Repeat

## Running the Code
First go to [Ducky Race](https://www.arcademics.com/games/ducky-race) and get ready to hit play now, make sure that you are using a blue duck.

Then, open up command line (or another terminal), shrink it, and move it to the top so that it doesn't cover the bottom half of the screen.

Once the game starts, run:
```
python ducky_race_AI.py
```