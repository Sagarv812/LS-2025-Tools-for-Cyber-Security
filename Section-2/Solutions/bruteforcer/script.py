import subprocess

def run_bruteforcer(password):
    
    result = subprocess.run(
        ['./bruteforcer'],
        input=password.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    return result.stdout.decode()

def main():
    
    with open('wordlist.txt', 'r') as f:
        passwords = sorted(line.strip() for line in f if line.strip())

    low = 0
    high = len(passwords) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = passwords[mid]
        print(f"Trying: {guess}") 

        output = run_bruteforcer(guess).lower()

        if 'flag{' in output:
            print(f"Found the flag:\n{output.strip()}")
            return
        elif 'low' in output:
            low = mid + 1
        elif 'high' in output:
            high = mid - 1
        

    print("Password not found.")

if __name__ == '__main__':
    main()
