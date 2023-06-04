def normalization_text(user_text):
    lower_user_text = user_text.lower()
    return lower_user_text

def input_error(user_text, normalization_user_text):
    user_text_split = user_text.split(" ")
    normalization_user_text_split = normalization_user_text.split(" ")
    tuple_cmd = ("hello", "add", "change", "phone", "show all", "exit", "good bye", "close")

    if not normalization_user_text.startswith(tuple_cmd):
        print(f"Wrong command {normalization_user_text_split[0]}. Please try again.")
        return False
    
    if normalization_user_text.startswith(("add", "change")):
        if not len(user_text_split) >= 3:
            print("Give me name and phone please")
            return False
        elif not user_text_split[1].isalpha() and not user_text_split[2].isdigit():
            print("Give me name and phone please")
            return False
        elif not user_text_split[1].isalpha():
            print("Enter user name")
            return False
        elif user_text_split[2][0] == "+":
            if not user_text_split[2][1:].isdigit():
                print("Enter phone")
                return False
        elif not user_text_split[2].isdigit():
                print("Enter phone")
                return False  
        
    if normalization_user_text.startswith("phone"):
        if not user_text_split[1].isalpha():
            print("Enter user name")
            return False
    return True

def cmd_hello():
    print("How can I help you?")

contact_dict = {}

def cmd_add(text):
    text_split = text.split(" ")
    if text_split[1] not in contact_dict:  
        contact_dict[text_split[1]] = text_split[2]
    #print(contact_dict)

def cmd_change(text):
    text_split = text.split(" ")
    if text_split[1] in contact_dict:  
        contact_dict[text_split[1]] = text_split[2]
    #print(contact_dict)

def cmd_phone(text):
    text_split = text.split(" ")
    name = text_split[1]
    print(contact_dict[name])

def cmd_show_all():
    sorted_contact_dict = {key: contact_dict[key] for key in sorted(contact_dict.keys())}
    for contact, phone in sorted_contact_dict.items():
        print(contact, phone)


def main():

    work = True
    while work:

        user_text = input()
        normalization_user_text = normalization_text(user_text)

        if input_error(user_text, normalization_user_text):

            if normalization_user_text.startswith("hello"):
                cmd_hello()
            elif normalization_user_text.startswith("add"):
                cmd_add(user_text)
            elif normalization_user_text.startswith("change"):
                cmd_change(user_text)
            elif normalization_user_text.startswith("phone"):
                cmd_phone(user_text)
            elif normalization_user_text.startswith("show all"):
                cmd_show_all()
            elif normalization_user_text.startswith(("exit", "good bye", "close")):
                work = False


main()