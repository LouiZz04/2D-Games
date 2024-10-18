# Flappy Bird

Created using SFML library in C++

## Installation

### For Windows

Clone repo and follow instructions from main [sfml-website](https://www.sfml-dev.org/tutorials/2.6/compile-with-cmake.php) to compile SFML on windows

### For Linux

1. Install required library using your package manager. For example for Debian run `sudo apt-get install libsfml-dev`

2. Compile the main file -in this case flappybird.cpp- run `g++ -c flappybird.cpp` creating a flappybird.o file

3. Link file to required libraries and create app. This file uses system, window, graphics and audio modules. Run `g++ flappybird.o -o sfml-app -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio`

4. Execute `./sfml-app`

for more detailed instructions go to [sfml-start-linux](https://www.sfml-dev.org/tutorials/2.6/start-linux.php)

