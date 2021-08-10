data_book = {}


def input_error(func):
    def inner():
        try:
            func()
        except ValueError:
            print('Please, use correct phone number!')
            func()
        except KeyError:
            print('Enter user name')
            func()
        except IndexError:
            print('Give me name and phone please')
            func()
    return inner


@input_error
def main():
    while True:
        message = input()
        conv_message = str(message).lower()
        if conv_message not in ['good', 'close', 'exit']:
            if conv_message == "hello":
                hello()
            elif (conv_message.split())[0] == 'add':
                add((message.split())[1].title(), message.split()[2])
            elif (conv_message.split())[0] == 'change':
                change((message.split())[1].title(), message.split()[2])
            elif (conv_message.split())[0] == 'phone':
                phone((message.split())[1].title())
            elif (conv_message.split())[0] == 'show':
                show()
            else:
                print('Please, write correct command!')
        else:
            break


def hello():
    print("How can I help you?")

def add(name, phone):
    data_book[name]=int(phone)

def change(name, phone):
    data_book[name]=int(phone)

def phone(name):
    print(data_book[name])

def show():
    for key, value in data_book.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()

