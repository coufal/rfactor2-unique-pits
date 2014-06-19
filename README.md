# rFactor2 UniquePits

Assigns each car to one (unique) pit and one (unique) garage. 

Ideal for leagues, since everyone needs their own pit to avoid conflicts.

## Features 

* You just have to add enough pit spots in DevMode and
this script will take care of the rest.
* Excess pits and garage spots will be removed automatically to avoid confusion.

## Usage

You can run the script from command line by typing:

`python UniquePits.py Input.AIW Output.AIW`

If you want to overwrite the old AIW, just omit the last argument:

`python UniquePits.py Input.AIW`

For more details, simply run with the *-h* argument.

## Prerequisites

* Python 3.3 (other versions should work as well)