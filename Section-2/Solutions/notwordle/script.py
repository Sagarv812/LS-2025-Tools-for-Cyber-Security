import subprocess
import re

def run_notwordle(password):
    
    result = subprocess.run(
        ['./notwordle'],
        input=password.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    return result.stdout.decode()


def parse_match_count(output):
    match = re.search(r'(\d+)\s*/\s*30', output)
    if match:
        return int(match.group(1))
    return -1




def main():

    password = ['a']*30
    matched = 0;
    for i in range(30):
        
        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_":
            password[i] = char
            stringPass = ''.join(password)
            print("Trying password: ", stringPass)
            output = run_notwordle(stringPass)
            print("Parsed match count: ", parse_match_count(output))
            if 'flag{' in output:
                print(output)
                exit(0)
            else:
                if(matched < parse_match_count(output)):
                    matched = parse_match_count(output)
                    break 


if __name__ == '__main__':
    main()