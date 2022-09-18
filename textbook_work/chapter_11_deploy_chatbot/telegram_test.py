import telegram
from api_IGNORE import API_key
bot = telegram.Bot(token=API_key)

# 'first_name': 'Test_bot', 'username': 'AugustTest_bot'
print(bot.get_me())
# it works :)
