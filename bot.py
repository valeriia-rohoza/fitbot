import os
import sys
import numpy as np
from numpy import ndarray
import telebot

# create token using BotFather in Telegram
API_KEY = os.getenv('API_KEY')

class Size:
    """ A class is used to collect an information about one size of body:
    Attributes:
        bust : float
            a number that corresponds to the measurements of the bust
        waist : float
            a number that corresponds to the measurements of the waist
        hips : float
            a number that corresponds to the measurements of the hips
        uk : int
            UK size
        us : int
            US size
        eu : int
            EU size
    """
    def __init__(self, bust, waist, hips, uk, us, eu):
        self.bust = bust
        self.waist = waist
        self.hips = hips
        self.uk = uk
        self.us = us
        self.eu = eu

# set arrays of sizes
bust_sizes : ndarray = np.array([31, 32, 33, 35, 37, 39, 41, 44])
waist_sizes: ndarray = np.array([24, 25, 26, 28, 30, 31, 33, 36])
hips_sizes : ndarray = np.array([33, 34, 35, 37, 39, 41, 43, 46])
uk_sizes : ndarray = np.arange(4, 20, 2)
us_sizes : ndarray = np.arange(0, 16, 2)
eu_sizes : ndarray = np.arange(32, 48, 2)

# make sure that the input data is of the same size
assert len(waist_sizes) == len(hips_sizes), "Check the number of input data for waist/hips parameters"
assert len(waist_sizes) == len(bust_sizes), "Check the number of input data for bust parameters"
assert len(waist_sizes) == len(uk_sizes), "Check the number of uk_sizes"
assert len(uk_sizes) == len(us_sizes), "Check the number of us_sizes"
assert len(uk_sizes) == len(eu_sizes), "Check the number of eu_sizes"

# initialize the sizes
dict_sizes = {}
for i in range(len(waist_sizes)):
    dict_sizes["s" + "%d" %i] = Size(bust_sizes[i], waist_sizes[i], hips_sizes[i], uk_sizes[i], us_sizes[i], eu_sizes[i])

# create a bot
bot = telebot.TeleBot(API_KEY)

# create a global dictionary of measurements linked to a chat id
dict_params = {}

# set what the bot does when a user sends /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi there! Let's find the right size of women's clothes for you. "
                          "Please send your measurements in the following format:\n\n"
                          "bust <number in inches> waist <number in inches> hips <number in inches>\n\n"
                                      "After that you can use commands /shorts to determine the size of the shorts or /shirt to find out your size of the shirt")
    dict_params[message.chat.id] = {}

def params(message):
    """
    This function decides whether a user inputs measurements in the format as it's asked.
    :param message
    :return: True -- if a user inputs at least six items (it asks for: "bust <number> waist <number> hips <number>"),
                        the 0th item is "bust", the 2nd is "waist", and the 4th is "hips"
            False -- otherwise
    """
    # split based on spaces
    request = message.text.split()
    if len(request) < 6 or request[0].lower() not in "bust" or request[2].lower() not in "waist" or request[4].lower() not in "hips":
        return False
    else:
        return True

# save the input measurements for the chat
@bot.message_handler(func=params)
def save_params(message):
    bust = float(message.text.split()[1])
    waist = float(message.text.split()[3])
    hips = float(message.text.split()[5])

    # store the chat id paired with measurements
    dict_params[message.chat.id] = {"bust": bust, "waist": waist, "hips": hips}

# set what a bot does when a user sends a command /shorts
@bot.message_handler(commands=['shorts'])
def shorts(message):
    if dict_params[message.chat.id]:
        # find a match between the input values and attributes of an instance of the class Size
        i = 0
        while dict_params[message.chat.id]["waist"] > dict_sizes["s" + "%d" % i].waist:
            i += 1
        while dict_params[message.chat.id]["hips"] > dict_sizes["s" + "%d" % i].hips:
            i += 1

        # create a dictionary to store the response
        dict = {}
        response = "Your size of the shorts is:\n"
        dict["UK"] = dict_sizes["s" + "%d" % i].uk
        dict["US"] = dict_sizes["s" + "%d" % i].us
        dict["EU"] = dict_sizes["s" + "%d" % i].eu

        for key in dict:
            response += f"{key}: {dict[key]}\n"

        # send the response with the size of shorts
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Don't forget to send your measurements first!")

# set what a bot does when a user sends a command /shirt
@bot.message_handler(commands=['shirt'])
def shirt(message):
    if dict_params[message.chat.id]:
        # find a match between the input values and attributes of an instance of the class Size
        i = 0
        while dict_params[message.chat.id]["bust"] > dict_sizes["s" + "%d" % i].bust:
            i += 1

        while dict_params[message.chat.id]["waist"] > dict_sizes["s" + "%d" % i].waist:
            i += 1

        while dict_params[message.chat.id]["hips"] > dict_sizes["s" + "%d" % i].hips:
            i += 1

        # create a dictionary to store the response
        dict = {}
        response = "Your size of the shirt is:\n"
        dict["UK"] = dict_sizes["s" + "%d" % i].uk
        dict["US"] = dict_sizes["s" + "%d" % i].us
        dict["EU"] = dict_sizes["s" + "%d" % i].eu

        for key in dict:
            response += f"{key}: {dict[key]}\n"

        # send the response with the size of shorts
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Don't forget to send your measurements first!")

bot.polling()