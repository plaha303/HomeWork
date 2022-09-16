# Task 1

class Queue:
    __data = list()
    __size = 0

    def __init__(self):
        pass

    def is_empty_is_full(self):
        if self.__size == 0:
            print('Queue is empty')
        else:
            print(f'\nQueue have {len(self.__data)} elements')

    def enqueue(self, element: any):
        self.__data.append(element)
        self.__size += 1

    def dequeue(self):
        if self.__size > 0:
            self.__data.pop(0)
            self.__size -= 1

    def show(self):
        for item in self.__data:
            print(item, end=', ')


queue = Queue()
print('***Queue program***')
print(f'*' * 40)
select = None
while select != 5:
    print('\nMenu:\n'
          '1. Queue check\n'
          '2. Add data\n'
          '3. Delete data\n'
          '4. Show queue\n'
          '5. Quit\n')
    select = int(input('Enter your choice: '))
    if select == 1:
        queue.is_empty_is_full()
    if select == 2:
        data = input('Enter data element: ')
        queue.enqueue(data)
    if select == 3:
        queue.dequeue()
    if select == 4:
        queue.show()


# Task 2

class QueuePriority:
    __data = list()
    __priority = list()
    __size = 0

    def __init__(self):
        pass

    def is_empty_is_full(self):
        if self.__size == 0:
            print('Queue is empty')
        else:
            print(f'\nQueue have {len(self.__data)} elements')

    def insert_with_priority(self, element: any, prior: int):
        self.__data.append(element)
        self.__priority.append(prior)
        self.__size += 1

    def pull_highest_priority_element(self):
        if self.__size > 0:
            max_priority = max(self.__priority)
            index_max_priority = self.__priority.index(max_priority)
            self.__data.pop(index_max_priority)
            self.__priority.pop(index_max_priority)
            self.__size -= 1

    def peek(self):
        if self.__size > 0:
            max_priority = max(self.__priority)
            index_max_priority = self.__priority.index(max_priority)
            return print(self.__data[index_max_priority])

    def show(self):
        for item in self.__data:
            data_index = self.__data.index(item)
            print(f'data: {item}, priority: {self.__priority[data_index]}')

    def priority(self):
        return self.__priority


queue = QueuePriority()
print('***Queue priority program***')
print(f'*' * 40)
select = None
while select != 6:
    print('\nMenu:\n'
          '1. Queue check\n'
          '2. Add data with priority\n'
          '3. Delete data with higher priority\n'
          '4. Show data with higher priority\n'
          '5. Show oll data with priority\n'
          '6. Quit\n')
    select = int(input('Enter your choice: '))
    if select == 1:
        queue.is_empty_is_full()
    if select == 2:
        data = input('Enter data element: ')
        priority = int(input('Input integer priority for data: '))
        if priority in queue.priority():
            priority = int(input('this priority exists, choose another: '))
        queue.insert_with_priority(data, priority)
    if select == 3:
        queue.pull_highest_priority_element()
    if select == 4:
        queue.peek()
    if select == 5:
        queue.show()


# Task 3

class UsersSteck:
    __user = list()
    __login = list()
    __password = list()
    __size = 0

    def __init__(self):
        pass

    def add_new_user(self, user: str, login: any, password: str):
        self.__user.append(user)
        self.__login.append(login)
        self.__password.append(password)
        self.__size += 1

    def del_user(self, user):
        if self.__size > 0:
            if user in self.__user:
                user_index = self.__user.index(user)
                self.__user.pop(user_index)
                self.__login.pop(user_index)
                self.__password.pop(user_index)
                self.__size -= 1
            else:
                print('User is not found')
        else:
            print('User steck is empty')

    def user_check(self, user):
        if user in self.__user:
            print(f'User {user} in "user stack"')
        else:
            print('User is not found')

    def change_login(self, user):
        if user in self.__user:
            user_index = self.__user.index(user)
            new_login = input('Enter new login: ')
            self.__login[user_index] = new_login
        else:
            print('User is not found')

    def change_password(self, user):
        if user in self.__user:
            user_index = self.__user.index(user)
            new_password = input('Enter new password: ')
            self.__password[user_index] = new_password
        else:
            print('User is not found')

    def show(self):
        for user in self.__user:
            user_index = self.__user.index(user)
            print(f'user: {user}, login: {self.__login[user_index]}, password: {self.__password[user_index]}')


users = UsersSteck()
print('***Users steck program***')
print(f'*' * 40)
select = None
while select != 7:
    print('\nMenu:\n'
          '1. Add user\n'
          '2. Delete user\n'
          '3. User check\n'
          '4. Change login\n'
          '5. Change password\n'
          '6. Show user steck\n'
          '7. Quit\n')
    select = int(input('Enter your choice: '))
    if select == 1:
        user_name = input('Input user name: ')
        login = input('Input login: ')
        password = input('Input password: ')
        users.add_new_user(user_name, login, password)
    if select == 2:
        user = input('Input user name: ')
        users.del_user(user)
    if select == 3:
        user = input('Input user name: ')
        users.user_check(user)
    if select == 4:
        user = input('Input user name: ')
        users.change_login(user)
    if select == 5:
        user = input('Input user name: ')
        users.change_password(user)
    if select == 6:
        users.show()
