import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from parser import Parser

def can_form_design(design, patterns_set):
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True 
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and design[j:i] in patterns_set:
                dp[i] = True
                break
    
    return dp[n]

if __name__ == "__main__":
    patterns, designs = Parser(file_path='input.txt').parse_sections(str)
    patterns, designs = patterns.split(', '), designs.splitlines()
    patterns_set = set(patterns)
    count = sum(1 for design in designs if can_form_design(design, patterns_set))
    print("Possible designs:", count)