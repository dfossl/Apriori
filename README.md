# Dylan Fossl
## Data Mining Assignment - Apriori
### Description
This assignment was to implment Apriori. The assignment was completed in python version python 3.9.0. [Apriori](https://en.wikipedia.org/wiki/Apriori_algorithm) is a classic frequement patter mining algorithm.

### Implementation
The goal was to implement Apriori as efficiently as possible with the constraint of not being able to hold the dataset in memory. I focused on time efficiency rather then space and used sets for contanst lookup times where appropriate. The main optimization of my algorthim is in candidate generation. Candidates are generated in a typical self join fashion but by using set operations strategically invalid candidate sets can be identified and ignored effciently.

### Input Data Format
The Data is expected to be as follows:\
4\
1	3	1 3 4\
2	3	2 3 5\
3	4	1 2 3 5\
4	2	2 5\

line 1 holds number of transactions.
Transactino lines are tab seperated with first column be id, second being number of items and third column being space seperated item list.

### Files
In the "Assignment_2" directory there are three python files titled **"Apriori.py"** and **"AprioriMain.py"**. Apriori.py is a class file that holds the function for my Apriori implmentation. AprioriMain.py will the file main file for running Apriori in command line.

To run Apriori in command line simply type in:
 >python3 AprioriMain.py -f [FileDirectory] -m [MinimumSupport] -o [OutputFileDirectory]


**FileDirectory** can be any file of valid format.

**MinimumSupport** must be a integer between 0-100.

**OutputDirectory** directory for output.
