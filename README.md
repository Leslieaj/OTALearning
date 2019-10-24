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

- In the result file of each group of the randomly generated DOTAs, we records our experiment results. Each line records the results of one DOTA in the group. The meanings of the numbers in a line are the **learning time**, the **location number**, the number of **membership queries with cache**, the number of **membership queries without cache**, the number of **equivalence queries with cache**, the number of **equivalence without cache**, the number of **explored table instances**, the number of **table instances to explore**, the number of **effective rows**. 

  - results of the group 3_2_10
  
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
  
  - results of the group 4_2_10

  | learning time      | location number | mem_q (cahce) | mem_q(no-cache) | eq_q(cache) | eq_q(no-cache) | explored | to explore | effective row |
  | ------------------ | --------------- | ------------- | --------------- | ----------- | -------------- | -------- | ---------- | ------------- |
  | 2.2155418395996094 | 4               | 111           | 2701            | 14          | 111            | 224      | 75         | 10            |
  | 2.763075590133667  | 4               | 67            | 5470            | 9           | 108            | 437      | 155        | 10            |
  | 1.5099635124206543 | 4               | 82            | 2836            | 12          | 126            | 225      | 113        | 11            |
  | 9.83553695678711   | 4               | 183           | 11106           | 24          | 347            | 795      | 323        | 16            |
  | 2.582578182220459  | 4               | 103           | 4420            | 14          | 212            | 381      | 43         | 8             |
  | 0.6428205966949463 | 4               | 68            | 2492            | 6           | 82             | 211      | 23         | 10            |
  | 1.0743918418884277 | 4               | 89            | 1607            | 13          | 60             | 152      | 30         | 8             |
  | 2.5383102893829346 | 4               | 149           | 10796           | 10          | 252            | 615      | 255        | 12            |
  | 3.052309513092041  | 4               | 143           | 3247            | 17          | 142            | 271      | 3          | 12            |
  | 48.551451206207275 | 4               | 345           | 99023           | 14          | 2072           | 2319     | 2073       | 17            |
  
  - results of the group 5_2_10
  
  | learning time      | location number | mem_q (cahce) | mem_q(no-cache) | eq_q(cache) | eq_q(no-cache) | explored | to explore | effective row |
  | ------------------ | --------------- | ------------- | --------------- | ----------- | -------------- | -------- | ---------- | ------------- |
  | 90.75118207931519  | 5               | 252           | 196893          | 14          | 2398           | 3541     | 16895      | 24            |
  | 2.1147031784057617 | 5               | 75            | 5423            | 9           | 344            | 437      | 63         | 9             |
  | 59.42913460731506  | 5               | 280           | 167949          | 17          | 5060           | 5305     | 13363      | 12            |
  | 162.7257435321808  | 4               | 310           | 232918          | 14          | 3884           | 11020    | 9927       | 20            |
  | 6.287023544311523  | 5               | 207           | 7643            | 13          | 357            | 582      | 21         | 11            |
  | 9.158974409103394  | 5               | 258           | 29261           | 12          | 642            | 1677     | 335        | 16            |
  | 8.337482213973999  | 5               | 144           | 37443           | 16          | 1129           | 3093     | 123        | 16            |
  | 7.267740726470947  | 6               | 357           | 15957           | 24          | 401            | 883      | 243        | 17            |
  | 7.617588520050049  | 5               | 220           | 25739           | 18          | 905            | 1414     | 111        | 16            |
  | 1.1311092376708984 | 5               | 118           | 2233            | 15          | 115            | 164      | 27         | 12            |

  - results of the group 6_2_10
  
  | learning time       | location number | mem_q (cahce) | mem_q(no-cache) | eq_q(cache) | eq_q(no-cache) | explored | to explore | effective row |
  | ------------------- | --------------- | ------------- | --------------- | ----------- | -------------- | -------- | ---------- | ------------- |
  | 2.093968629837036   | 5               | 73            | 2607            | 10          | 113            | 233      | 27         | 8             |
  | 31.803288459777832  | 5               | 268           | 92407           | 10          | 287            | 859      | 4607       | 17            |
  | time out  (>10 min) |                 |               |                 |             |                |          |            |               |
  | memory out  (>8Gb)  |                 |               |                 |             |                |          |            |               |
  | 5.4659576416015625  | 6               | 225           | 10060           | 12          | 306            | 747      | 39         | 20            |
  | 11.497714281082153  | 5               | 333           | 29362           | 20          | 162            | 948      | 768        | 24            |
  | 331.7036316394806   | 6               | 583           | 618808          | 23          | 1915           | 27349    | 439        | 19            |
  | 27.443557500839233  | 6               | 708           | 158235          | 30          | 810            | 5099     | 53         | 32            |
  | memory out (>8Gb)   |                 |               |                 |             |                |          |            |               |
  | 8.724203109741211   | 6               | 248           | 6798            | 12          | 179            | 308      | 55         | 20            |

  - results of the group 4_4_20
  
  | learning time      | location number | mem_q (cahce) | mem_q(no-cache) | eq_q(cache) | eq_q(no-cache) | explored | to explore | effective row |
  | ------------------ | --------------- | ------------- | --------------- | ----------- | -------------- | -------- | ---------- | ------------- |
  | 71.67515420913696  | 4               | 564           | 87724           | 40          | 1940           | 3583     | 239        | 35            |
  | memory out  (>8Gb) |                 |               |                 |             |                |          |            |               |
  | 131.56549453735352 | 4               | 389           | 63216           | 30          | 1533           | 2992     | 693        | 28            |
  | 222.2726845741272  | 4               | 420           | 527324          | 27          | 12923          | 24359    | 45075      | 19            |
  | memory out  (>8Gb) |                 |               |                 |             |                |          |            |               |
  | 46.41304874420166  | 4               | 312           | 46358           | 27          | 1220           | 2223     | 483        | 26            |
  | 143.35004138946533 | 4               | 310           | 322200          | 30          | 6998           | 15369    | 9071       | 22            |
  | memory out (>8Gb)  |                 |               |                 |             |                |          |            |               |
  | 209.42800068855286 | 4               | 231           | 49634           | 31          | 2145           | 3014     | 65         | 25            |
  | memory out (>8Gb)  |                 |               |                 |             |                |          |            |               |