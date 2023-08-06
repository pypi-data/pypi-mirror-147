import random
number = random.randint(1,100)
while True:
    shout = input('Guess my number:')
#"Выдает ошибку и перезапускает ввод, если введена буква"
    if shout.isalpha():
        print('Invalid, please write only numbers')
        continue
#"Ниже блок убирает ошибку и перезапускает ввод, если ничего не введено"
    try:
        shout = round(eval(shout))
    except ValueError:
        print('Please, enter only digit!')     
        continue
    if shout == number:
        print('Yeahhhhhhh')
        break
    elif shout <= (number + 5) and shout >= (number - 5):
        print('Approximately 5')  
    elif shout <= ((number + 6 and number +10)) and shout >= ((number - 6 and number - 10)):
        print('Approximately 10')  
    elif shout <= ((number + 11 and number +20)) and shout >= ((number - 11 and number - 20)):
        print('Approximately 20')
    elif shout <= ((number + 21 and number +30)) and shout >= ((number - 21 and number - 30)):
        print('Approximately 30')
    else:
        print('Far, try again')