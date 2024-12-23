import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from parser import Parser

def count_ways_to_form_design(design, patterns_set):
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1 
    for i in range(1, n + 1):
        for j in range(i):
            if design[j:i] in patterns_set:
                dp[i] += dp[j]
    return dp[n]

if __name__ == "__main__":
    patterns, designs = Parser(file_path='input.txt').parse_sections(str)
    patterns = patterns.split(', ')
    designs = designs.splitlines()
    patterns_set = set(patterns)

    total_ways = sum(count_ways_to_form_design(design, patterns_set) for design in designs)

    print("Total ways to arrange designs:", total_ways)
