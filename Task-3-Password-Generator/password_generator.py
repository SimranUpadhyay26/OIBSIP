import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):

char_pool = ""
if use_letters:
    char_pool += string.ascii_letters 
if use_numbers:
    char_pool += string.digits       
if use_symbols:
    char_pool += string.punctuation    
if not char_pool:
    print("Error: No character types selected.")
    return None


password = ''.join(random.choice(char_pool) for _ in range(length))
return password

def main():
print("=== Password Generator ===")

while True:
    try:
        length = int(input("Enter password length (e.g., 8): "))
        if length <= 0:
            print("Password length must be a positive number.")
        else:
            break
    except ValueError:
        print("Please enter a valid number.")

use_letters = input("Include letters? (y/n): ").lower() == 'y'
use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
use_symbols = input("Include symbols? (y/n): ").lower() == 'y'


password = generate_password(length, use_letters, use_numbers, use_symbols)
if password:
    print(f"\nGenerated Password: {password}")

if __name__ == "__main__":
main()







