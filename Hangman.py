HANGMAN_ASCII_ART = ("""
       _    _
      | |  | |
      | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
      |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \\
      | |  | | (_| | | | | (_| | | | | | | (_| | | | |
      |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                           __/ |
                          |___/
""")

MAX_TRIES = 6

HANGMAN_PHOTOS = {
    0: """
     \nx-------x\
""",
    1:
        """x-------x
           |
           |
           |
           |
           |""",

    2: """
     x-------x
     |       |
     |       0
     |
     |
     |
""",

    3: """
     x-------x
     |       |
     |       0
     |       |
     |
     |
""",

    4: """
     x-------x
     |       |
     |       0
     |      /|\\
     |
     |
""",

    5: """
     x-------x
     |       |
     |       0
     |      /|\\
     |      /
     |
""",

    6: """
     x-------x
     |       |
     |       0
     |      /|\\
     |      / \\
     |
"""
}


def print_hangman(num_of_tries):
    """
    הפונקציה מדפיסה את אחד משבעת המצבים של האיש התלוי, בעזרת משתנה שמייצג את מספר הנסיונות הכושלים.
    """
    print(HANGMAN_PHOTOS[num_of_tries])


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    פונקציה בוליאנית שמקבלת תו ורשימת אותיות שהמשתמש ניחש בעבר. הפונקציה בודקת שני דברים:
    את תקינות הקלט והאם חוקי לנחש אות זו (כלומר, השחקן לא ניחש אות זו בעבר) ומחזירה אמת או שקר בהתאם.
    """
    if len(letter_guessed) > 1 or not letter_guessed.isalpha():
        return False
    elif letter_guessed.lower() in old_letters_guessed:
        return False
    elif (len(letter_guessed) == 1 and letter_guessed.isalpha()) and letter_guessed not in old_letters_guessed:
        return True
    else:
        return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
         הפונקציה משתמשת בפונקציה check_valid_input כדי לדעת אם התו תקין ולא ניחשו אותו בעבר או התו אינו תקין
         ו/או נמצא כבר ברשימת הניחושים. אם התו איננו תקין או שכבר ניחשו את התו בעבר, הפונקציה מדפיסה
          את התו X (כאות גדולה),מתחתיו את רשימת האותיות שכבר נוחשו ומחזירה שקר.
          אם התו תקין ולא ניחשו אותו בעבר - הפונקציה מוסיפה את התו לרשימת הניחושים ומחזירה אמת.
         """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print("X")
        print(*old_letters_guessed, sep=' -> ')
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """
    פונקציה שמחזירה מחרוזת אשר מורכבת מאותיות ומקווים תחתונים. המחרוזת מציגה את האותיות מתוך הרשימה old_letters_guessed
    שנמצאות במחרוזת secret_word במיקומן המתאים, ואת שאר האותיות במחרוזת (אותן השחקן טרם ניחש) כקווים תחתונים.
    """
    word = ""
    for i in secret_word:
        if i in old_letters_guessed:
            word += i
        else:
            word += ' _ '
    return word


def check_win(secret_word, old_letters_guessed):
    """
    פונקציה בוליאנית שמחזירה אמת אם כל האותיות שמרכיבות את המילה הסודית
    נכללות ברשימת האותיות שהמשתמש ניחש. אחרת, הפונקציה מחזירה שקר
    """
    for c in secret_word:
        if c not in old_letters_guessed:
            return False
    return True


def choose_word(path, index):
    """
    הפונקציה מקבלת כפרמטרים: מחרוזת המייצגת נתיב לקובץ טקסט המכיל מילים מופרדות ברווחים,
    ומספר שלם המייצג מיקום של מילה מסוימת בקובץ. הפונקציה מחזירה מילה במיקום שהתקבל כארגומנט לפונקציה (index).
    """
    with open(path, "r") as words_input_file:
        secret = words_input_file.read()
        secret_list = secret.split(",")
        if index > len(secret_list):
            chosen_word_location = index % len(secret_list)
            chosen_word = secret_list[chosen_word_location]
        else:
            chosen_word = secret_list[index]
        return chosen_word


def main():
    old_letters_guessed = []
    num_of_tries = 0
    print(HANGMAN_ASCII_ART, MAX_TRIES)
    path = input("Enter path to text file with words separated by ',':\n")
    index = int(input("Enter index please:\n"))
    secret_word = choose_word(path, index)
    print(show_hidden_word(secret_word, old_letters_guessed))
    while not check_win(secret_word, old_letters_guessed) and num_of_tries < MAX_TRIES:
        letter_guessed = input("Guess a letter: ")
        num_of_tries += 1
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed not in secret_word:
                print("X")
                print_hangman(num_of_tries)
            print(show_hidden_word(secret_word, old_letters_guessed))

    if check_win(secret_word, old_letters_guessed):
        print("WIN!")
    else:
        print("LOSE!")
        print("The secret word was: " + secret_word)


if __name__ == "__main__":
    main()
