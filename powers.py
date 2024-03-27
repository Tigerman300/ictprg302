#!/usr/bin/python3

def main():
    n = int(input('Enter a number: '))
    for i in range(n + 1):
        square = i * i
        cubed = i * i * i
        print(f"The number {i}, it's square is {square} and it's cube is {cubed}.")

if __name__ == '__main__':
    main()