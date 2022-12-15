# Advent of Code

My entries for advent of code! https://adventofcode.com/

According to its author, [Eric Wastl](http://was.tl/), Advent of Code is a series of "small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like." Eric hosts this event every December (since 2015 it looks like), hence the "Advent" of code. The problems are all loosely related to each other via a little Christmas-themed story, which makes things kind of fun.

This is my first time participating in this event. I am using python to solve the puzzles. I considered using javascript, which would have been some nice exercise, but seeing as this is my first time and I would really like to finish each puzzle on the day of publishing, I am sticking with python.

Chatting with other programmers about the problems has been great fun! I have been chatting with attendees of the [NormConf](https://normconf.com/) conference about the daily puzzles on Slack. These attendees are mostly data scientists and data engineers, so there is a lot of python going on with this crowd (and a few brave Rust users). I have found that submitting my own solution, and then looking at other solutions is teaching me a lot. Off the top of my head, some neat python tricks I have learned are:

- using eval() to directly convert raw text to python data structures is fun, but dangerous! ast.literal_eval() is a safer alternative that generally only evaluates data structures.
- the decorator @dataclass is really useful for making classes that are primarily data structures. If you still need to init() something, you can define a _post_init_() method.
- lots of cool libraries. Curses is a cool (if intimidating) package for rendering animations in the terminal.

I have also been animating some of my solutions! [Pyxel](https://github.com/kitao/pyxel) is a rad little library which is a full virtual-console powered via python. I have found this to be the easiest way, by far, to make little data-powered gifs (check out the solutions below). Not every solution lends itself well to an animation, so I haven't been forcing it.

If you are interested in some of my learnings and work, scroll down below. I am trying to summarize some of my learnings from each day.

## Running on your own system.

You will need python on your system to run my solutions.

Generally, you need to cd to the specific directories to run code in order for file paths to resolve correctly. eg:

```
advent_of_code> cd day2
advent_of_code\day2> python day2.py
```

~~No dependencies besides standard library in python.~~ I am using pyxel to animate a lot of these now. You will need an older version which still supports the "flip" command:

``` 
python -m pip install pyxel==1.8.2
```

I recommend setting up a virtual environment and installing pyxel there, rather than doing a global install.

## Solution discussion

I am using the library [pyxel](https://github.com/kitao/pyxel) to animate some of my solutions. Check them out below! Spoilers if you are still working on these.


### Day 1
A pretty gentle start to the event. Day 1 sets the stage for the rest of the problems - generally, we are provided with a flat text file containing data of some sort, and we need to read it in and do something with it.

Day 1 really is just an exercise in reading data and parsing it. We are provided a series of numbers and line breaks, and asked to group and sum the numbers, separating based on the line breaks. This problem really only took a few minutes.

![Day 1](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day1.gif)

Not super exciting for day 1. We are basically just going through a list of numbers and keeping track of the totals until there is a line break. When we hit a line break, create a new entry and start counting again.

Note tht I AM storing every single number in a list. It would be much more memory efficient to just keep track of the top N entries. Python makes it so easy to stick these things in a list though, it's hard not to.

### Day 2
Day 2 also presents us with a large flat file of data, but this time we need to convert different letters into different values. Specifically, we need to "parse" a series of Rock-Paper-Scissors matches, and we are provided with notation that somewhat resembles [chess notation](https://en.wikipedia.org/wiki/Chess_notation). 

Another easy one. I kept my code readable by using explicitly named constants.

### Day 3
So far so easy. Today, we basically just needed to identify the common letter in different separate strings. Python sets make this easy, since we can just take the intersection of sets and, if our problem has been posed correctly, we are left with only a single letter which is a member of each set.

Sets can use some shorthand that makes them easy to read:

```python
a: set = {1,2,3,4}
b: set = {4,5,6}
a & b # returns {4}
a | b # returns {1, 2, 3, 4, 5, 6, 7}
a - b # returns {1,2,3}
a ^ b # symmetric difference, returns non-overlapping elements, {1, 2, 3, 5, 6, 7}
```

### Day 4


### Day 8

![Day 8](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day8.gif)

Combing the forest for trees that are visible from the outside.


### Day 9

![Day 9](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day9.gif)

Pulling a rope around. This one takes very long! I did not record the whole thing.

### Day 10

![Day 10](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day10.gif)

Pretty easy one today. Fun one to render though!

### Day 11

![Day 11](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day11.gif)

One round of passing. This one took a while to solve!

### Day 12

![Day 12](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day12.gif)

A* to find a path up the mountain. BFS is probably quicker just in terms of coding things up, but I wanted to practice doing an A* search.

![Day 12 BFS](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day12_bfs.gif)

Just by switching out our Priority Queue with a regular queue, we get BFS search.

### Day 14

![Day 14](https://github.com/paloblanco/advent_of_code/blob/master/gifs/day14.gif)

GREAT day to animate.