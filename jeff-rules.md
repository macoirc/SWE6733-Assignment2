Constraints:
The `Quality` of an item is never negative
The `Quality` of an item is never more than `50`
  test: 0 <= Q <= 50
  partitions: Q - [ {-99,-1}, 0, {1,50}, {51,99} ]

Parameters:
Once the sell by date has passed, `Quality` degrades twice as fast
  test: if D < 0 then Q-2
  partitions: D - [ {-99,-1}, 0, {1,99} ]

Exceptions:
"Aged Brie" actually increases in `Quality` the older it gets
  test: Q(B) + 1
  partitions: D - [ {-99,-1}, 0, {1,99} ]
"Sulfuras" never has to be sold or decreases in `Quality`
"Sulfuras" is always `Quality` of `80`
  tests: Q(S) == 80 ,  D1 == D2
  partitions: D - [ {-99,-1}, 0, {1,99} ]
"Backstage passes" increase in `Quality` as its `SellIn` value approaches
  - `Quality` increases by `2` when there are `10` days or less
    test: if 5 < D <= 10 then Q+2
  - `Quality` increases by `3` when there are `5` days or less
    if 0 <= D <= 5 then Q+3
  - `Quality` drops to `0` after the concert
    if D < 0 then Q=0
    partitions: D - [ {-99,-1}, {0,5}, {6,10}, {11,99} ]

Future Improvement:
"Conjured" items degrade in `Quality` twice as fast as normal items