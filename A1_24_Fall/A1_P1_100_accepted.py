import sys


"""
Author: ac_coder
Time: 2024/9/29
"""
if __name__ == '__main__':
    n, m, p = list(map(int, sys.stdin.readline().split()))
    a = list(map(int, sys.stdin.readline().split()))

    # total: Sum of current array
    # numValues: Number of values in input array, which is a dict to store key-value pairs
    # distinctSet: Values that can make contribution of another distinct value
    # if we select it and multiply each of them by either 1 or −1
    total = 0
    numValues = {}
    distinctSet = set()

    # Initialize total, numValues and distinctSet before we make operations
    for i in range(n):
        total += a[i]
        numValues[a[i]] = numValues[a[i]] + 1 if a[i] in numValues else 1
        # For distinctSet, there are two cases that can make variation of the number of distinct values
        # Case 1: Number of a[i] is 2, and number of -a[i] is 0, then we can make one of a[i] -> -a[i]
        # i.e. the number of distinct values is added by 1, and insert a[i] into distinctSet
        if numValues[a[i]] == 2 and -a[i] not in numValues:
            distinctSet.add(a[i])
        # Case 2: Number of a[i] is 1, and number -a[i] is in distinctSet, then -a[i] should be removed from distinctSet
        if numValues[a[i]] == 1 and -a[i] in distinctSet:
            distinctSet.remove(-a[i])

    # Make m operations
    for _ in range(m):
        row = list(map(int, sys.stdin.readline().split()))
        op = row[0]
        # Update the value of a[k] by using the formula given in the problem
        if op == 1:
            k, x, y, c = row[1], row[2], row[3], row[4]
            # Mark old value and new value
            oldValue = a[k - 1]
            newValue = ((x * x + k * y + 5 * x + p) % p) * c
            a[k - 1] = newValue
            # Update the delta value, i.e. newValue - oldValue to total
            total += newValue - oldValue
            if oldValue == newValue:
                continue

            # Update the number of oldValue
            numValues[oldValue] -= 1
            # For distinctSet, there are two cases that can make variation of the number of distinct values
            # Case 1: Number of oldValue is 1, and number oldValue is in distinctSet,
            # then a[i] cannot make contribution of the number of distinct values,
            # then it should be removed from distinctSet
            if numValues[oldValue] == 1 and oldValue in distinctSet:
                distinctSet.remove(oldValue)
            # Case 2: Number of oldValue is 0, then it should be removed from numValues
            if numValues[oldValue] == 0:
                del numValues[oldValue]
                # If number of -oldValue is more than or equal to 2, and -oldValue is not in distinctSet,
                # then we can make one of -oldValue -> oldValue
                # i.e. the number of distinct values is added by 1, and insert -oldValue into distinctSet
                if -oldValue in numValues and numValues[-oldValue] >= 2 and -oldValue not in distinctSet:
                    distinctSet.add(-oldValue)

            # Update the number of newValue
            numValues[newValue] = numValues[newValue] + 1 if newValue in numValues else 1
            if numValues[newValue] == 2 and -newValue not in numValues:
                distinctSet.add(newValue)
            if numValues[newValue] == 1 and -newValue in distinctSet:
                distinctSet.remove(-newValue)

        # Query the sum of all elements in the sequence
        elif op == 2:
            print(total)

        # Query the maximum number of distinct values in the sequence if each element is multiplied by either 1 or −1
        # We can flip the sign of some elements and count the maximum number of distinct numbers
        # Therefore, sum(number of numValues and number of distinctSet) is the result
        elif op == 3:
            print(len(numValues) + len(distinctSet))
"""
Some typical test cases
5 5 3
0 0 0 1 -2
3
1 5 1 2 -1
3
1 3 2 1 1
3

10 10 5
-1 -2 2 -3 2 0 -4 3 3 -3
3
1 2 4 4 -1
2
1 3 1 2 -1
3
2
3
1 2 4 4 1
3
1 4 4 0 -1

4 1 10
2 2 -2 -2
3

4 1 10
1 -1 1 -1
3

11 1 10
2 2 -2 -2 2 1 -1 1 -1 -3 -3 
3

5 10 5
2 2 0 0 -2
"""