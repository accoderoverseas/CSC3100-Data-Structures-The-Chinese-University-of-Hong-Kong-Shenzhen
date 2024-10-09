import collections
import sys


"""
Author: ac_coder
Time: 2024/9/29
"""
if __name__ == '__main__':
    n, q = map(int, sys.stdin.readline().split())
    perm = list(map(int, sys.stdin.readline().split()))
    l = list(map(int, sys.stdin.readline().split()))
    r = list(map(int, sys.stdin.readline().split()))

    # pos: Position of values in input array, which is a dict to store key-value pairs
    # The problem guarantees that values in input array are all distinct, then their position can be stored in the dict
    pos = collections.defaultdict(int)
    for i in range(n):
        pos[perm[i]] = i

    # res: Marks whether current split process with q operations is valid(1=valid, 0=invalid)
    res = 1

    # Case 1: From bottom to top, the top operation should cover the whole permutation, otherwise it is invalid
    if pos[l[0]] != 0 or pos[r[0]] != n - 1:
        res = 0
    else:
        # segmentDict: a dict to represent interval that can be splitted
        segmentDict = collections.defaultdict(int)
        # Follow the process in the problem from bottom to top
        for i in range(q - 1, -1, -1):
            # Get current position interval [curLeft, curRight]ß
            curLeft, curRight = pos[l[i]], pos[r[i]]

            # Case 2: curLeft > curRight, which is invalid
            if curLeft >= curRight:
                res = 0
                break

            # Case 3: curLeft cannot be in an interval except its' left point
            # Case 4: curRight cannot be in an interval except its' right point
            for preLeft in segmentDict:
                preRight = segmentDict[preLeft]
                if preLeft + 1 <= curLeft <= preRight:
                    res = 0
                    break
                if preLeft <= curRight <= preRight - 1:
                    res = 0
                    break
            if res == 0:
                break

            # Case 5: Merge intervals, and update right point of merged interval
            # Count number of merged intervals
            numMergedIntervals = 0
            mergedIntervals = []
            for preLeft in segmentDict:
                preRight = segmentDict[preLeft]
                if curLeft <= preLeft <= curRight:
                    numMergedIntervals += 1
                    mergedIntervals.append([preLeft, preRight])

            # Case 5.1: A merge operation cannot merge three or more intervals
            if numMergedIntervals >= 3:
                res = 0
                break
            # Case 5.2: If a merge operation merges two intervals, then there cannot be gap between the two intervals,
            # or between one of them and [curLeft, curRight]
            elif numMergedIntervals == 2:
                if mergedIntervals[0][1] + 1 != mergedIntervals[1][0] or mergedIntervals[0][0] != curLeft or mergedIntervals[1][1] != curRight:
                    res = 0
                    break
                del segmentDict[mergedIntervals[0][0]]
                del segmentDict[mergedIntervals[1][0]]
                segmentDict[curLeft] = curRight
            # Case 5.3: If a merge operation merges one interval,
            # then its' left or right point should equal to curLeft or curRight
            elif numMergedIntervals == 1:
                if mergedIntervals[0][0] != curLeft and mergedIntervals[0][1] != curRight:
                    res = 0
                    break
                if curLeft == mergedIntervals[0][0]:
                    segmentDict[curLeft] = curRight
                else:
                    del segmentDict[mergedIntervals[0][0]]
                    segmentDict[curLeft] = curRight
            # Case 5.4: If a merge operation does not merge any interval, then store [curLeft, curRight] directly
            else:
                segmentDict[curLeft] = curRight

            # Case 6: The interval [curLeft, curRight] cannot cover a whole existed interval
            for preLeft in segmentDict:
                preRight = segmentDict[preLeft]
                if curLeft < preLeft and curRight > preRight:
                    res = 0
                    break
            if res == 0:
                break

            # Finally, sort the segment dict
            segmentDict = dict(sorted(segmentDict.items(), key=lambda k: k[0]))
    print(res)
"""
Some typical test cases
6 3
6 3 4 1 2 5
6 4 4
5 5 2
=> 1

7 3
7 6 3 4 1 2 5
6 4 4
5 5 2
=> 0

7 3
6 3 4 1 2 5 7
6 4 4
5 5 2
=> 0

7 3
1 2 3 4 5 6 7
1 3 5
7 7 6
=> 0

8 3
1 2 3 4 5 6 7 8
1 1 5
8 4 8
=> 1

9 4
1 2 3 4 5 6 7 8 9
1 1 5 6
9 4 9 8
=> 0

9 4
1 2 3 4 5 6 7 8 9
1 1 5 6
9 4 9 9
=> 1

12 7
1 2 3 4 5 6 7 8 9 10 11 12
1 1 10 1 1 1 5
12 9 12 7 4 3 7
=> 1

7 3
1 2 3 4 5 6 7
1 3 5
7 7 7
=> 1

7 3
1 2 3 4 5 6 7
1 3 5
7 7 6
=> 0

9 3
1 2 3 4 5 6 7 8 9
1 4 1
9 8 3
=> 0

15 3
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
1 8 3
15 15 5
=> 0

6 3
1 2 3 4 5 6
1 3 1
6 6 2
=> 1

6 3
6 3 4 1 2 5
6 3 1
5 4 5
=> 0

12 4
1 2 3 4 5 6 7 8 9 10 11 12
1 1 5 9
12 4 8 12
=> 0

12 3
1 2 3 4 5 6 7 8 9 10 11 12
1 9 1
12 12 6
=> 0
"""