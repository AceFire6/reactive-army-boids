Reactive Formation-Based Armies for Games
---

Author: Jethro Muller

### Introduction

These two programs were produced as part of an undergraduate research course.
My topic was the extension of Craig Reynold's Boids algorithm to be used
to control formations in strategy games.

To do this I used the force-accumulator and weighted average systems used
in his flocking algorithms and used them as the basis for the unit movement.
The unit movement was also largely based on the flocking.

An additional layer was added to the mix in the form of a formation object
to control and manage the formation. The unit's movements are all still
behaviour based, however, where precisely they go is determined by the formation
as it controls the waypoints they head towards.

#### Installation

To run this, all you will need to do is install `pygame`.  
`apt-get install pygame`


### Instructions

* Formation Maker:  
	* Run: `python ./formation_designer.py`
	* `Left Click (1st time)` place the center point of the formation.
	* `Left Click (2nd time)` place the direction point of the formation.
	* `Left Click (nth time)` place a unit.
	* `Esc` to quit.
	* `CTRL-S` to save the formation.
	* `CTRL-O` to open and edit a formation.

* Simulation:  
	* Run: `python ./main.py`
	* `CTRL-O` to open a formation file.
	* `Esc` to quit.
	* `R` to reset the simluator.
	* `Right Click` give the formation a move command.
	* `Left Click (1st time)` set the start point of an enemy.
	* `Left Click (2nd time)` set the end of the enemies path and spawn it.

