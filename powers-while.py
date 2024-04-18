#!/usr/bin/python3

def square(num):
    return num * num
    
def cube(num):
    return num * num * num

def main():
    n = int(input('Enter a number: '))
    seq = 1
    while seq <= n:
        squ = square(seq)
        cub = cube(seq)
        print(f"The number is {seq}, its {squ} is 1 and its cube is {cub}.")
        seq += 1

if __name__ == '__main__':
    main()