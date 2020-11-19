from random import Random
str = ''
chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
length = len(chars) - 1
random = Random()
for i in range(16):
    str+=chars[random.randint(0,length)]
print(str)