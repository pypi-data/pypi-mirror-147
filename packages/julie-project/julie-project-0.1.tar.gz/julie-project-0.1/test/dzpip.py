while True: 
     name = input('Введите имя:')
     age = int(input('Введите возраст:'))
     if age < 18: 
           print ("Привет {}".format(name), 'тебе до 18 осталось', (18-int(age)),'лет' )
     elif age >= 18:
        print (f"Привет {name}", 'ты старше 18' )