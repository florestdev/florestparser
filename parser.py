import os
try:
    from telethon.sync import TelegramClient
 
    from colorama import Fore
 
    from telethon.tl.functions.messages import GetDialogsRequest
    from telethon.tl.types import InputPeerEmpty
    import pandas as pd
    import socks
except ImportError:
    input(f'У вас отсутствуют нужные библиотеки. Установить?')
    os.system('pip install telethon')
    os.system('pip install colorama')
    os.system('pip install pandas')
    os.system('pip install openpyxl')
# Получим данные от Telegram Users API.
api_id =  0000000 # индентификатор пользователя.
api_hash = '...'  # HASH код.
phone_number = '+70000000000' # ваш номер телефона.

client = TelegramClient('session_123___', api_id, api_hash)

client.start(phone_number)

banner = f"""{Fore.GREEN}
 _____  _                          _    ____
|  ___|| |  ___   _ __   ___  ___ | |_ |  _ \   __ _  _ __  ___   ___  _ __
| |_   | | / _ \ | '__| / _ \/ __|| __|| |_) | / _` || '__|/ __| / _ \| '__|
|  _|  | || (_) || |   |  __/\__ \| |_ |  __/ | (_| || |   \__ \|  __/| |
|_|    |_| \___/ |_|    \___||___/ \__||_|     \__,_||_|   |___/ \___||_|
"""

print(f'{banner}\n\nПарсер, созданный для людей.')
chats = []
last_date = None
size_chats = 200
groups=[]

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=size_chats,
    hash = 0
    )
)
chats.extend(result.chats)
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
    
print(f'{Fore.YELLOW}Выберите номер группы из перечня:')
i=0
for g in groups:
    print(F'{Fore.GREEN}{str(i)} - {g.title}')
    i+=1
g_index = input("Введите нужную цифру: ")
target_group=groups[int(g_index)]

print(f'{Fore.YELLOW}Узнаём пользователей...')
all_participants = client.get_participants(target_group)

print(f'{Fore.YELLOW}Начинаем парсить {all_participants.total} участников.')

i_ = 1

id = []
usernames = []
names = []
surnames = []
phone = []
scam = []
premium = []
activity = []

for user in all_participants:
    id.append(f'{user.id}')
    usernames.append(f'@{user.username}')
    names.append(f'{user.first_name}')
    surnames.append(f'{user.last_name}')
    phone.append(f'{user.phone}')
    scam.append(f'{user.scam}')
    premium.append(f'{user.premium}')
    activity.append(f'{user.status}')

print(f'{Fore.GREEN}Парсинг был проведен успешно.')
directory = input(f'В какую директорию сохранить `members.xlsx`?')
print(f'{Fore.YELLOW}Запись ников в `members.xlsx`...')

data = {
    "id":id,
    "usernames":usernames,
    'names':names,
    'surnames':surnames,
    'phones':phone,
    'scam':scam,
    'premium':premium,
    'activity':activity
}
df = pd.DataFrame(data)

# Сохраняем DataFrame в Excel
writer = pd.ExcelWriter(f'{directory}/members.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False)
writer.close()

print(f'{Fore.GREEN}Ники находятся в файле `members.txt` в папке {directory}.')

client.disconnect()
