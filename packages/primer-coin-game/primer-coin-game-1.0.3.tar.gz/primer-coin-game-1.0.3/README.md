# Python Implementation of Primer Coin Game

Python implementation of Primer's Coin Game which can be used for testing and simulations.
To find out more about the game see [Primer's video](https://www.youtube.com/watch?v=QC91Bf8hQVo/) and try the [original game](https://primerlearning.org/).

## Getting Started

### Dependencies

To run the simulator you just need Python 3.6+ installed. 

### Installing

Go to https://www.python.org/ for instruction how to install Python on your machine.
The package can be found on [PyPi](https://pypi.org/project/primer-coin-game/) so you can use pip to install the package:
```
# python -m pip install --upgrade primer-coin-game
```

Another way to install it is by manually cloning the repo. To clone you can use:
```
# git clone https://github.com/ErikKarlen/primer-coin-game-python.git
```

### Executing program

Try running the example simulator in a terminal, e.g using:
```
# cd primer-coin-game-python
# python simulate.py
```
It will simulate the game many times using the generate_action function to determine what to do in different cases and finally print the max score it managed to get.
Feel free to try and implement your own generate_action function to see if you can make it more efficient and get a higher score.

## Authors

Erik Karlén

## Version History

* 1.0
  *  Initial working game and simulator

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledegments

* [Primer](https://www.youtube.com/watch?v=QC91Bf8hQVo) - Thanks for creating the original game and making awesome videos!
