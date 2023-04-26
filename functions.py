import discord
import random
import datetime
import schedule
import os
import time, asyncio
import sqlite3
import psycopg2
from functions import *
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv


#deprecated birthday methods that caused errors
# async def dailyCheckIfMemberWithBirthday(birthdayRole, roleID, guild, formattedDay, databaseCursor):
# 	for row in databaseCursor.execute('SELECT userID, birthday FROM users'):
# 		if row[1] == formattedDay:
# 			# if someone's birthday matches today's date, then get their user ID
# 			birthdayHuman = guild.get_member(row[0])
# 			await birthdayHuman.add_roles(birthdayRole)
# 			defaultChannel = guild.get_channel(387429109049065474)
# 			await defaultChannel.send('We have a <@&' + str(roleID) + '>')
#
# async def dailyClearBirthdayHumanRole(birthdayRole, guild):
# 	for member in guild.members:
# 		if birthdayRole in member.roles:
# 			await member.remove_roles(birthdayRole)

def getUserIDFromUserAt(userAtHandle):
	if str(userAtHandle[2]) == '&':
		userID = str(userAtHandle[3:])
		userID = int(userID[:-1])
	elif str(userAtHandle[2]) != '!':
		userID = str(userAtHandle[2:])
		userID = int(userID[:-1])
	else:
		userID = str(userAtHandle[3:])
		userID = int(userID[:-1])
	return userID

def getUserInfo(userIDOrNamePassed, databaseCursor):
	# Passed info is a user's @ handle
	if userIDOrNamePassed[1] == "@":
		userID = getUserIDFromUserAt(userIDOrNamePassed)

		for row in databaseCursor.execute("SELECT * FROM users WHERE userID=?", (userID,)):
			userInfo = row

	# Passed info is a user's ID number
	elif isinstance(userIDOrNamePassed, int):
		for row in databaseCursor.execute("SELECT * FROM users WHERE userID=?", (userIDOrNamePassed)):
			userInfo = row
	# Passed info is just a user's name (must match name column in database)
	else:
		userName = userIDOrNamePassed.lower()
		for row in databaseCursor.execute("SELECT * FROM users WHERE name=? COLLATE NOCASE", (userName,)):
			userInfo = row

	return userInfo

def getUserAt(userID):
	atUserIDString = str('<@!' + str(userID) + '>')

	return atUserIDString

def giveUserPoints(userGiving, userReceiving, pointQuantity, databaseCursor):
	userGivingID = userGiving[0]
	userGivingNewTotal = userGiving[3] + int(pointQuantity)
	databaseCursor.execute("UPDATE users SET cringeScore=? WHERE userID=?", (userGivingNewTotal, userGivingID))

	userReceivingID = userReceiving[0]
	userReceivingNewTotal = userReceiving[3] - int(pointQuantity)
	databaseCursor.execute("UPDATE users SET cringeScore=? WHERE userID=?", (userReceivingNewTotal, userReceivingID))


def getEmoteID(emoteName):
	emoteID = "\\" + emoteName
	emoteID = emoteID[1:]

	return emoteID

def convertNamesToIDs(listOfNames):
	listOFIDs = []
	for name in listOfNames:
		userIDs = name.id
		listOFIDs += [userIDs]

	return listOFIDs

def updateCringeRecordsAdd(messageAuthor, databaseCursor):
	for row in databaseCursor.execute("SELECT cringeScore FROM users WHERE userID=?", (messageAuthor,)):
		currentCringeScore = row
	currentCringeScore = currentCringeScore[0] + 1
	databaseCursor.execute("UPDATE users SET cringeScore=? WHERE userID=?", (currentCringeScore, messageAuthor,))

def updateCringeRecordsSubtract(messageAuthor, databaseCursor):
	for row in databaseCursor.execute("SELECT cringeScore FROM users WHERE userID=?", (messageAuthor,)):
		currentCringeScore = row
	currentCringeScore = currentCringeScore[0] - 1
	databaseCursor.execute("UPDATE users SET cringeScore=? WHERE userID=?", (currentCringeScore, messageAuthor,))