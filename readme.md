# Advent of Code

My entries for advent of code! https://adventofcode.com/

Generally, you need to cd to the specific directories to run code in order for file paths to resolve correctly.

~~No dependencies besides standard library in python.~~ I am using pyxel to animate a lot of these now. You will need an older version which still supports the "flip" command:

``` 
python -m pip install pyxel==1.8.2
```

# Solution gifs

I am using the library [pyxel](https://github.com/kitao/pyxel) to animate some of my solutions. Check them out below! Spoilers if you are still working on these.


## Day 1

![Day 1](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day1.gif)

Not super exciting for day 1. We are basically just going through a list of numbers and keeping track of the totals until there is a line break. When we hit a line break, create a new entry and start counting again.

Note tht I AM storing every single number in a list. It would be much more memory efficient to just keep track of the top N entries. Python makes it so easy to stick these things in a list though, it's hard not to.

## Day 8

![Day 8](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day8.gif)

Combing the forest for trees that are visible from the outside.


## Day 9

![Day 9](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day9.gif)

Pulling a rope around. This one takes very long! I did not record the whole thing.