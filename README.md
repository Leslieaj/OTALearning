# OTALearning

A prototype on learning one-clock timed automata.

### Overview

This tool is dedicated to learning deterministic one-clock timed automata (DOTAs) which is a subclass of timed automata with only one clock. In 1987, Dana Angluin introduced the L* Algorithm for learning regular sets from queries and counterexamples. The tool implement an Angluin-style active learning algorithm on DOTAs. This branch is the normal teacher situation. The `master` and  `dev` branches are the smart teacher situation with and without the accelerating trick, respectively.

### Installation & Usage

#### Prerequisite

- Python 3.5.* (or high)


#### Installation

- Just download.

It's a pure Python program.  We have test it on Ubuntu 16.04 64bit with Python 3.5.2.

#### Usage

For example

```shell
python3 learnota.py experiments/example.json
```

- `learnota.py` is the main file of the program.

- The target DOTA is stored in a JSON file, in this example, `example.json` . The details are as follows.

  ```json
  {
    "name": "A",
    "l": ["1", "2"],
    "sigma": ["a", "b"],
    "tran": {
  	    "0": ["1", "a", "(1,3)", "n", "2"],
  	    "1": ["1", "b", "[0,+)", "r", "1"],
  	    "2": ["2", "b", "[2,4)", "r" "2"]
    },
    "init": "1",
    "accept": ["2"]
  }
  ```

  - "name" : the name of the target DOTA;
  - "s" : the set of the name of locations;
  - "sigma" : the alphabet;
  - "tran" : the set of transitions in the following form:
    - transition id : [name of the source location, action, guard, reset, name of the target location];
    - "+" in a guard means INFTY​;
    - "r" means resetting the clock, "n" otherwise.
- "init" : the name of initial location;
  - "accept" : the set of the name of accepting locations.
  
#### Output

- During the learning process, the following three numbers are printed, the number of the explored table, the number of the table to be explored, the number of effective row in $\bm{S}$ and $\bm{R}$.

- We do not print the current table in this case since there are so many explored table instances during the learning process.

- If we learn the target DOTA successfully, then the **finial table instance**, the **learnt COTA**, and the **corresponding DOTA** will be printed on the terminal. Additionally, the number of **membership queries (with and without cache)**, the number of **equivalence queryies(with and without cache)**, the number of the **explored table instances**, the number of the **table instances to be explored**, and the **learning time** will also be given. 

- In the result file of each group of the randomly generated DOTAs, we records our experiment results. Each line records the results of one DOTA in the group. The meanings of the numbers in a line are the **learning time**, the **location number**, the number of **membership queries with cache**, the number of **membership queries without cache**, the number of **equivalence queries with cache**, the number of **equivalence without cache**, the number of **explored table instances**, the number of **table instances to explore**, the number of **effective rows**. For example, the result for group `3_2_10` is represented in the following table.

  | learning time       | location number | mem_q (cahce) | mem_q(no-cache) | eq_q(cache) | eq_q(no-cache) | explored | to explore | effective row |
  | ------------------- | --------------- | ------------- | --------------- | ----------- | -------------- | -------- | ---------- | ------------- |
  | 1.4397876262664795  | 3               | 120           | 3437            | 12          | 108            | 257      | 97         | 9             |
  | 0.395519495010376   | 3               | 43            | 551             | 7           | 20             | 47       | 18         | 6             |
  | 3.6728410720825195  | 3               | 167           | 7575            | 14          | 173            | 562      | 200        | 15            |
  | 0.32153940200805664 | 3               | 70            | 1636            | 7           | 59             | 163      | 11         | 10            |
  | 0.21793413162231445 | 3               | 50            | 580             | 5           | 19             | 60       | 18         | 5             |
  | 0.5875141620635986  | 3               | 95            | 1098            | 10          | 65             | 94       | 6          | 9             |
  | 0.8570766448974609  | 3               | 85            | 1835            | 11          | 98             | 119      | 162        | 8             |
  | 0.5399534702301025  | 3               | 47            | 664             | 8           | 26             | 61       | 19         | 6             |
  | 0.498793363571167   | 3               | 60            | 613             | 7           | 31             | 58       | 15         | 6             |
  | 0.3032650947570801  | 3               | 100           | 717             | 7           | 14             | 70       | 3          | 14            |
  
  
  
   
