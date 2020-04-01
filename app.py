#Libraries to be import START
import random
from flask import Flask, request, g, session, render_template, redirect, url_for, flash
from messenger_syntax.bot import Bot
import os
import json
import time, string, random, re
#import pymongo
#from pymongo import MongoClient
#import Mongo#import Mongo.py
#from NLU import nlp
#from collections import Counter #install collections
#Libraries to be import END

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
#MONGO_TOKEN = os.environ['MONGO_DB']

bot = Bot (ACCESS_TOKEN)
'''To be edit
cluster = MongoClient(MONGO_TOKEN)
db = cluster["DrPedia"]
users = db["users"]
patient = db["patient"]
'''

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		"""Before allowing people to message your bot, Facebook has implemented a verify token
		that confirms all requests that your bot receives came from Facebook.""" 
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	#if the request was not get, it must be POST and we can just proceed with sending a message back to user
	else:
		# get whatever message a user sent the bot
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					if message['message'].get('text'):
						if message['message'].get('quick_reply'):
							received_qr(message)  
						else: #else if message is just a text
							received_text(message)
					#if user sends us a GIF, photo,video, or any other non-text item
					elif message['message'].get('attachments'):
						#TO BE EDIT
						#bot.send_text_message(sender_id,get_message())
						pass
				elif message.get("postback"):  # user clicked/tapped "postback" button in earlier message
					received_postback(message)
					
	return "Message Processed"

def verify_fb_token(token_sent):
	#take token sent by facebook and verify it matches the verify token you sent
	#if they match, allow the request, else return an error 
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge"), 200
	else:
		return "Verification token mismatch", 403
	return render_template('index.html')
#===============================================================Personal Website==============================================================================

# Terms of Service page, required for Facebook App Review


#---------------------------------------------------------------Conversation Start---------------------------------------------------------------------
image_url = 'https://raw.githubusercontent.com/clvrjc2/drpedia/master/images/'
GREETING_RESPONSES = ["Hi", "Hey", "Hello there", "Hello", "Hi there"]
GREETING_RESPONSES_Time = ["morning", "noon", "afternoon", "evening"] 
greet = random.choice(GREETING_RESPONSES)

#Greetings, persisten menu, get started button

#if user tap a button from a regular button
def received_postback(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	payload = event["postback"]["payload"]
	
	first_name = get_users_info(sender_id,'first_name')#Get sender's Firstname ex. [Je]
	last_name = get_users_info(sender_id,'last_name')#Get sender's Lastname ex. [Becerro]
	#profile_pic = get_users_info(sender_id,'profile_pic')#Get sender's profile picture ex. [https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/p200x200/13055603_10105219398495383_8237637584159975445_n.jpg?oh=1d241d4b6d4dac50eaf9bb73288ea192&oe=57AF5C03&__gda__=1470213755_ab17c8c8e3a0a447fed3f272fa2179ce]
	'''Need Facebook Approval
	locale = get_users_info(sender_id,'locale')#Get sender's locale ex. [en_US] for translation PH not supported as of [3/30/2020]
	timezone = get_users_info(sender_id,'timezone')#Get sender's Timezone, number relative to GMT ex. [-7]
	gender = get_users_info(sender_id,'gender')#Get sender's Gender ex. [male] || [female]
	'''
	#Get started button tapped{
	if payload=='start':
		bot.send_text_message(sender_id,'{} {}, this is Je Ar your IT and social media marketing companion.'.format(greet,first_name))
		bot.send_action(sender_id, 'typing_on')#typing...
		time.sleep(1.5)
		gladToMeetMe = [{"content_type":"text","title":"Nice to meet you😊!","payload":'pmyou'}]
		bot.send_quick_replies_message(sender_id, 'Are you glad to meet me {}?'.format(first_name),gladToMeetMe) 
		#enter welcome message
		
	#Persistent Menu Buttons        
	if payload=='start_over':
		bot.send_text_message(sender_id,'Hello World')
	#Social Media Accounts are URL
	#Information
	if payload=='pm_services':
		bot.send_text_message(sender_id,"Currently in development.. but you can check my page for more updates")
	if payload=='pm_aboutme':
		bot.send_text_message(sender_id,"Currently in development.. but you can check my page for more updates")
	if payload=='pm_appoinment':
		bot.send_text_message(sender_id,"Currently in development.. but you can check my page for more updates")
	if payload=='pm_support':
		bot.send_text_message(sender_id,"This section is for client support only.")
		clientAlready = {"content_type":"text","title":"Yes","payload":'yes_client'},{"content_type":"text","title":"no","payload":'no_client'}
		bot.send_quick_replies_message(sender_id, 'Already a client?',clientAlready) 
	if payload=='pm_website':
		bot.send_text_message(sender_id,"My website currently in development.. but you check my page for more updates")
	if payload=='pm_poweredby':
		bot.send_text_message(sender_id,'This Messenger Bot is developed by Je Ar Becerro.')
	
#if user tap a button from a quick reply
def received_qr(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	qr = event["message"]["quick_reply"]["payload"]
	
	first_name = get_users_info(sender_id,'first_name')#Get sender's Firstname ex. [Je]
	last_name = get_users_info(sender_id,'last_name')#Get sender's Lastname ex. [Becerro]
	
	if qr=='pmyou':
		bot.send_text_message(sender_id,"I'm glad to meet you too {} 😊.".format(first_name))
		bot.send_action(sender_id, 'typing_on')#typing...
		time.sleep(1)
		bot.send_text_message(sender_id,"I am here to assist you, interms of Website developement - Chatbot development and Social Media Marketing.")
		bot.send_action(sender_id, 'typing_on')#typing...
		time.sleep(1)
		bot.send_text_message(sender_id,"What do you want to know ?")


#if user send a message in text
def received_text(event):
	sender_id = event["sender"]["id"]        # the facebook ID of the person sending you the message
	recipient_id = event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
	text = event["message"]["text"]
	
		
	
#Conversation End

#To get information from facebook users
def get_users_info(sender_id,whatInfo):
	user_info = bot.get_user_info(sender_id)
	if user_info is not None: 
		if whatInfo == 'first_name':
			return user_info['first_name']
		
		if whatInfo == 'profile_pic':
			return user_info['profile_pic']
		#Need approval by facebook
		'''
		if whatInfo == 'locale':
			return user_info['locale']
		
		if whatInfo == 'timezone':
			return user_info['timezone']
		
		if whatInfo == 'gender':
			return user_info['gender']
		'''
	return ''
'''
#To generate dynamic greeting if its morning noon evening, a repeative user or new
def sayHiTimeZone(user):
    user_now = getUserTime(user)
    if recentChat(user):
        response = ["Hi again", "Hey hey hey again", "What's up", "Hey there again"]
        if user_now.hour > 5 and user_now.hour < 12:
            response.extend(["Shiny day isn't it", "What a morning", "Morningggg"])
        elif user_now.hour < 19:
            response.extend(["How's your afternoon", "Afternoooooon", "What a day"])
        elif user_now.hour < 4 or user_now.hour > 22:
            response.extend(["Hmm... you're a night owl", "Long night hah", "You know, science has shown that sleeping early is good for you health", "The night is still young, I'm here"])
        else:
            response.extend(["Good evening", "What's rolling for dinner"])
        return oneOf(response)
    if user_now.hour > 5 and user_now.hour <= 12:
        return "Good morning"
    elif user_now.hour > 12 and user_now.hour < 19:
        return "Good afternoon"
    else:
        return "Good evening"
'''	

def Get_Started(greeting_text):
	#Greetings 
	greetings =  {"greeting":[
		  {
			  "locale":"default",
			  "text": greeting_text
			}
		]}
	bot.set_greetings(greetings)
	#Get started button
	gs ={ 
			  "get_started":{
				"payload":'start'
			  }
		}
	bot.set_get_started(gs)
	#bot.remove_persistent_menu()#to edit persistent menu first remove it and then put the Pesistent_Menu() back
	#Persistent_Menu()
	false=False
	true=True
	pm_menu = {
				"persistent_menu": [
					{
						"locale": "default",
						"composer_input_disabled": false,
						"call_to_actions": [
							{#Star Over Menu
								"type": "postback",
								"title": "Start Over ⤴️",
								"payload": "start_over"
							},
							{#See More Menu
						        "title":"See More 👀..",
						        "type":"nested",
						        "call_to_actions":[
						            {#Social Media Account -See More Menu
						            "title":"Social Media Accounts 📱..",
						             "type":"nested",
							      "call_to_actions":[
								    {#Youtube -Social Media Account -See More Menu
								            "title":"Youtube 📺",
								            "type":"web_url",
								            "url":"https://www.youtube.com/channel/UC2MLFAzNB3sPMtFrrHWZAaQ?view_as=subscriber",
								            "webview_height_ratio": "full"
							            },
							            {#Instagram -Social Media Account -See More Menu
								            "title":"Instagram 📷",
								            "type":"web_url",
								            "url":"https://www.instagram.com/jearbecerro/",
								            "webview_height_ratio": "full"
							            },
							            {#Facebook -Social Media Account -See More Menu
								            "title":"Facebook 🥸📘",
								            "type":"web_url",
								            "url":"https://www.facebook.com/JeArGaming/",
								            "webview_height_ratio": "full"
							            },
							            {#Github -Social Media Account -See More Menu
								            "title":"GitHub 🐱",
								            "type":"web_url",
								            "url":"https://github.com/jearbecerro",
								            "webview_height_ratio": "full"
							            } 
							            ],
							        },#End Social Media Account
								 #Wesite currently in development
								{"title":"Visit My Website ℹ️ 🚧",
								    "type":"web_url",
								    "url":"https://jearbecerro.herokuapp.com/",
								     "webview_height_ratio": "full"
								}#End My Website
					        ]
					        },
							{#Information -See More Menu
						            "title":"Information 📝..",
						             "type":"nested",
							        	"call_to_actions":[
								        {#My Services -Information -See More Menu
								        "title":"Services 🎖️",
							            "type":"postback",
							            "payload":"pm_services"
							            },
							            {#About Me -Information -See More Menu
							            "title":"About Me 💁‍♂️",
							            "type":"postback",
							            "payload":"pm_aboutme"
							            },
							            {#Appointment -Information -See More Menu
							            "title":"Schedule Appointment 🗓️",
							            "type":"postback",
							            "payload":"pm_appoinment"
							            },
							            {#Client Support -Information -See More Menu
							            "title":"Client Support 🧗",
							            "type":"postback",
							            "payload":"pm_support"
							            }
							            ],
							        },#End Information
						]
					}
				] 
			}
	bot.set_persistent_menu(pm_menu)
	print(bot.set_persistent_menu(pm_menu))
	print('testing')

greetInGetStarted = "Hi {{user_first_name}}!, Thank you for getting in touch with me. Please send me any question you may have."
Get_Started(greetInGetStarted)#Dynamic Greetings

#bot.remove_get_started()
#bot.remove_persistent_menu()

if __name__ == "__main__":
	app.run()
 
