from datetime import date, timedelta
import string

# --- PART 1: CAESAR CIPHER FUNCTIONS (Secret Code Maker) ---
# These functions encode and decode text using a secret shift number.

import string

def encode(input_text, shift):
    alphabet = list(string.ascii_lowercase)
    out = []
    for ch in input_text:
        if ch.isalpha():
            # always shift using LOWERCASE only
            base = ord('a')
            idx = (ord(ch.lower()) - base + shift) % 26
            out.append(chr(base + idx))
        else:
            out.append(ch)
    return (alphabet, "".join(out))

def decode(input_text, shift):
    """Decrypts input_text using Caesar cipher. Returns only the decoded text."""
    alphabet = list(string.ascii_lowercase)
    decoded_text = ""
    # This is the "shifted" alphabet used for encoding
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    
    for char in input_text:
        if 'a' <= char <= 'z':
            # Find the position in the *shifted* alphabet, and map back to the original
            old_index = shifted_alphabet.index(char)
            decoded_text += alphabet[old_index]
        elif 'A' <= char <= 'Z':
            # Handle uppercase letters
            lower_char = char.lower()
            old_index = shifted_alphabet.index(lower_char)
            shifted_lower_char = alphabet[old_index]
            decoded_text += shifted_lower_char.upper()
        else:
            # Keep all other characters the same
            decoded_text += char
            
    return decoded_text

# --- PART 2: BANK ACCOUNT CLASSES ---

class BankAccount:
    """The main class for a bank account."""
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        self.name = name
        self.ID = ID
        self.balance = balance
        
        # Set default creation_date if None is provided
        if creation_date is None:
            self.creation_date = date.today()
        else:
            # Rule: Cannot be a future date
            if creation_date > date.today():
                # Rule: Must raise an exception if it is a future date
                raise Exception("Account creation date cannot be in the future.")
            self.creation_date = creation_date
        
    def deposit(self, amount):
        # Rule: negative deposit amounts are not allowed
        if amount < 0:
            print("Error: Negative deposit amounts are not allowed.")
            return

        self.balance += amount
        # Rule: display the resulting balance
        print(f"Deposit of ${amount:.2f} successful. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        # Base class withdraw has no special rules, but must display the new balance
        self.balance -= amount
        print(f"Withdrawal of ${amount:.2f} processed. New balance: ${self.balance:.2f}")
        
    def view_balance(self):
        # Method returns the balance
        return self.balance


class SavingsAccount(BankAccount):
    """A savings account subclass with extra rules."""
    def withdraw(self, amount):
        # Rule 1: withdrawals are only permitted after 180 days (about 6 months)
        if (date.today() - self.creation_date).days < 180:
            print("Withdrawal denied: Account must exist for at least 180 days.")
            return
            
        # Rule 2: overdrafts (negative account balance) are not permitted
        if self.balance - amount < 0:
            print("Withdrawal denied: Overdrafts are not permitted on this Savings Account.")
            return

        # If rules are passed, use the parent class logic
        super().withdraw(amount)


class CheckingAccount(BankAccount):
    """A checking account subclass with an overdraft fee rule."""
    def withdraw(self, amount):
        
        # Perform withdrawal first
        self.balance -= amount
        
        # Rule: overdrafts are permitted, but incur a $30 fee
        if self.balance < 0:
            fee = 30
            self.balance -= fee
            print(f"Overdraft detected. A ${fee:.2f} fee has been applied.")
            
        # Rule: display the resulting balance
        print(f"Withdrawal of ${amount:.2f} processed. New balance: ${self.balance:.2f}")
