import os
import sys
import numpy as np
from numpy import ndarray
import telebot

# create token using BotFather in Telegram
API_KEY = os.getenv('API_KEY')

class Shorts:
    """ A class is used to collect an information about one size of shorts:
    Attributes:
        waist : float
            a number that corresponds to the measurements of the waist
        hips : float
            a number that corresponds to the measurements of the hips
        uk : int
            UK size of these shorts
        us : int
            US size of these shorts
        eu : int
            EU size of these shorts
    """
    def __init__(self, waist, hips, uk, us, eu):
        self.waist = waist
        self.hips = hips
        self.uk = uk
        self.us = us
        self.eu = eu

# set arrays of sizes
waist_sizes: ndarray = np.array([24, 25, 26, 28, 30, 31, 33, 36])
hips_sizes = np.array([33, 34, 35, 37, 39, 41, 43, 46])
uk_sizes = np.arange(4, 20, 2)
us_sizes = np.arange(0, 16, 2)
eu_sizes = np.arange(32, 48, 2)

# make sure that the input data is of the same size
assert len(waist_sizes) == len(hips_sizes), "Check the number of input data for waist/hips parameters"
assert len(waist_sizes) == len(uk_sizes), "Check the number of uk_sizes"
assert len(uk_sizes) == len(us_sizes), "Check the number of us_sizes"
assert len(uk_sizes) == len(eu_sizes), "Check the number of eu_sizes"

# initialize the sizes
dict_shorts = {}
for i in range(len(waist_sizes)):
    dict_shorts["sh" + "%d" %i] = Shorts(waist_sizes[i], hips_sizes[i], uk_sizes[i], us_sizes[i], eu_sizes[i])

# create a bot
bot = telebot.TeleBot(API_KEY)

# set what the bot does when a user sends \start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi there! Let's find the right size of women's shorts for you.\n"
                          "Please send your measurements in the following format:\n"
                          "waist <number in inches> hips <number in inches>")
def shorts_params(message):
    """
    This function decides whether the bot sends the size of the shorts as a response to a message.
    :param message
    :return: True -- if a user inputs at least four items (it asks for: "waist <number> hips <number>"),
                        the first item is "waist" and the third one is "hips"
            False -- otherwise
    """
    # split based on spaces
    request = message.text.split()
    if len(request) < 4 or request[0].lower() not in "waist" or request[2].lower() not in "hips":
        return False
    else:
        return True

# outputs size of the shorts
@bot.message_handler(func=shorts_params)
def send_shorts(message):
    waist = float(message.text.split()[1])
    hips = float(message.text.split()[3])

    # find a match between the input values and attributes of an instance of the class Shorts
    i = 0
    while waist > dict_shorts["sh" + "%d" %i].waist:
        i += 1

    while hips > dict_shorts["sh" + "%d" %i].hips:
        i += 1

    # create a dictionary to store the response
    dict = {}
    response = "Your size is:\n"
    dict["UK"] = dict_shorts["sh" + "%d" %i].uk
    dict["US"] = dict_shorts["sh" + "%d" %i].us
    dict["EU"] = dict_shorts["sh" + "%d" %i].eu

    for key in dict:
        response += f"{key}: {dict[key]}\n"

    # send the response with the size of shorts
    bot.send_message(message.chat.id, response)

bot.polling()
