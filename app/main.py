import get_config as gc
import sys
import re
import verification as ver
from Requests.mailing_request import Mailing_request
from Requests.mailing_response import Mailing_response
from log.logging import create_log

def menu_operation() -> int:
    """
    Выводит меню выбора действий.
    """
    message_error: str = "Неверный формат ввода.\n"
    while(True):
        print("Введите номер пункта.\n1.Создать рассылку.\n2.Выйти.")
        client_chose: str = input()
        try:
            chose = int(client_chose)
        except ValueError:
            print(message_error)
            
        if(chose == 1):
            creating_mailing()
        elif(chose == 2):
            sys.exit()
        else:
            print(message_error)

def conversion_number(number: str) -> str:
    """Форматирует номер"""
    if(len(number) == 10):
        number = "+7" + number
    elif(len(number) == 11):
        number = "+7" + number[1:]

    return number

def read_number(role: str) -> str: 
    """
    Читает введённый номер. Включает проверку на коррекстность.
    """
    mask = gc.get_config()["mask_number"]["regular_expression"]
    pattern = r"" + mask

    while True: 
        number = input(f"Введите номер телефона {role}. Exit для выхода:")
        number = number.replace(" ", "")
        if(number == "Exit"):
            return "-"

        match = re.match(pattern, number)
        if(bool(match)):
            break
        else:
            print("Некорректный номер.")
            return "-" #Для тестов.
    
    number = conversion_number(number)
    return number

def check_data_mail(sender_number: str, kecipient_number: str, massage: str ) -> int:
    print(f"Телефон отправителя: {sender_number}\nТелефон получателя: {kecipient_number}\nСообщение: {massage}\nДанные корректы?(y/n)")
    if input() != 'y':
        return 0
    else:
        return 1

def read_data_mail() -> list[str]:
    sender_number = read_number("Отправителя")
    if(sender_number == "-"):
        return '','',''
    recipient_number = read_number("Получателя")
    if(recipient_number == "-"):
        return '','',''
    message = input("Введите сообщение: ")

    return sender_number, recipient_number, message

def creating_mailing() -> int:
    """
    Создает рассылку.
    """
    sender_number, recipient_number, message = read_data_mail()
    if sender_number == '' or check_data_mail(sender_number, recipient_number, message) == 0:
        return 0

    dict_data = {"sender":sender_number, "recipient": recipient_number, "message":message}
    request = Mailing_request(dict_data)
    
    create_log("create request", "creating_mailing", "Creating a mailing list")
    response = request.make_request()
    if not response:
        return 0
    
    print(f"Результат: Код запроса - {response.code_response}, Информация - {response.body_response}\n")  
    return 1      
    
if __name__ == "__main__":
    if ver.login_verification() == 0:
        sys.exit() 
        
    menu_operation()
    
    

     



  




