"""
Where we load the world, declare the global vars, some const,…
"""
import sys
import asyncio
import os
import discord
from math import *
from random import *
from time import *

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
UP = 5
DOWN = 6

#### ! put your discord bot token here: ! ###
TOKEN = 'I’m not telling you'

global players_channels
players_channels = {}

global world
world = {}

global toSend
toSend = []

global players
players = {}

global connected
connected = set()

client = discord.Client()
