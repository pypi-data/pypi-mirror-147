from re import findall
from random import randint, choice
from json import loads, dumps, JSONDecodeError
from base64 import b64encode
from requests import post,get
from datetime import datetime
from rubika_lib.encryption import encryption
from PIL import Image
from io import BytesIO
from pathlib import Path

class client:
	web = {
		"app_name": "Main",
		"app_version" : "4.0.4",
		"platform": "Web",
		"package": "web.rubika.ir",
		"lang_code": "fa"
	} # clients
	android = {
		"app_name" : "Main",
		"app_version" : "2.9.5",
		"platform": "Android",
		"package": "ir.resaneh1.iptv",
		"lang_code": "fa"
	}
		
class Bot:
	def __init__(self, auth):
		self.auth = auth
		#res = get("https://raw.githubusercontent.com/Snipe4Kill/library-update/main/rubikaLibraryUpdate.json")
#		if res.status_code == 200:
#			res = loads(res.text)
#			if res["update"] != "1.1.0": print("Please order the library\npip install rubika-lib --upgrade\nUpdate!" +  '\n\n' + "لطفا کتابخانه را با دستور\npip install rubika-lib --upgrade\nآپدیت نمایید!"); exit()
		if len(self.auth) != 32: print("Your auth is wrong!\nخطا، شناسه حساب کاربری شما اشتباه است!"); exit()
		print("The Rubika Robot Library began operations\nMade by Shayan Heydari\nstarting...\n")
		self.enc = encryption(auth)
		
	@staticmethod
	def __getUrl__():
		return "https://messengerg2c64.iranlms.ir/" # return random host
		
	@staticmethod
	def _parse(mode:str, text:str):
		results = []
		if mode.upper() == "HTML":
			realText = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","")
			bolds = findall("<b>(.*?)</b>",text)
			italics = findall("<i>(.*?)</i>",text)
			monos = findall("<pre>(.*?)</pre>",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		elif mode.lower() == "markdown":
			realText = text.replace("**","").replace("__","").replace("`","")
			bolds = findall(r"\*\*(.*?)\*\*",text)
			italics = findall(r"\_\_(.*?)\_\_",text)
			monos = findall("`(.*?)`",text)

			bResult = [realText.index(i) for i in bolds]
			iResult = [realText.index(i) for i in italics]
			mResult = [realText.index(i) for i in monos]

			for bIndex,bWord in zip(bResult,bolds):
				results.append({
					"from_index": bIndex,
					"length": len(bWord),
					"type": "Bold"
				})
			for iIndex,iWord in zip(iResult,italics):
				results.append({
					"from_index": iIndex,
					"length": len(iWord),
					"type": "Italic"
				})
			for mIndex,mWord in zip(mResult,monos):
				results.append({
					"from_index": mIndex,
					"length": len(mWord),
					"type": "Mono"
				})

		return results
		
	def sendMessage(self, chat, text, metadata=[], parse_mode=None, message_id=None):
		""" auth.sendMessage("guid", "your text") """ # send Message To group or Channel Or ...
		try:
			inData = { "method":"sendMessage", "input":{ "object_guid":chat, "rnd":f"{randint(100000,999999999)}", "text":text, "reply_to_message_id":message_id }, "client": client.web }
			if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
			if parse_mode != None :
				inData["input"]["metadata"] = {"meta_data_parts":Bot._parse(parse_mode, text)}
				inData["input"]["text"] = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else text.replace("**","").replace("__","").replace("`","")
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass
		
	def reciveChatsUpdate(self):
		""" auth.reciveChatsUpdate() """ # Chats Update
		try:
			time_stamp = str(round(datetime.today().timestamp()) - 200)
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"getChatsUpdates", "input":{ "state":time_stamp,}, "client": client.android }))},url=Bot.__getUrl__()).json().get("data_enc"))).get("data").get("chats")
		except: pass
		
	def reciveMessages(self, guid ,min_id):
		""" auth.reciveMessages("guid", "min_id") """ # Get Group or Channel or pv Messages
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getMessagesInterval", "input":{ "object_guid":guid, "middle_message_id":min_id },"client": client.web }))},url=Bot.__getUrl__()).json().get("data_enc"))).get("data").get("messages")
		except: pass
		
	def reciveGroupInfo(self, guid):
		# recive Group Info
		try:
			return loads(self.enc.decrypt(post( json={ "api_version":"5", "auth": self.auth, "data_enc": self.enc.encrypt(dumps({ "method":"getGroupInfo", "input":{ "group_guid": guid, }, "client": client.web }))}, url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass

	def reciveChannelInfo(self, guidChannel):
		try:
			return loads(self.enc.decrypt(post( json={ "api_version":"5", "auth": self.auth, "data_enc": self.enc.encrypt(dumps({ "method":"getChannelInfo","input":{ "channel_guid": guidChannel,}, "client": client.web }))}, url=Bot.__getUrl__()).json()["data_enc"])) # Get Channel Info, as name or ...
		except: pass
		
	def editMessage(self, message_id, guid, newText):
		try:
			return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"editMessage", "input":{ "message_id": message_id, "object_guid": guid, "text": newText }, "client":{ "app_name":"Main", "app_version":"4.0.4","platform":"Web", "package":"web.rubika.ir", "lang_code":"fa"}}))},url=Bot.__getUrl__())
		except: pass
		
	def joinGroup(self, link):
		try:
			link = link[24:]
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"joinGroup","input":{"hash_link": link},"client": client.web}))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass
		
	def leaveGroup(self, group_guid):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"leaveGroup","input":{"group_guid": group_guid},"client": client.web}))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass
		
	def updateProfile(self, bio, first_name, last_name):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({"method":"updateProfile","input":{"bio": bio,"first_name": first_name,"last_name": last_name,"updated_parameters": ["first_name", "last_name", "bio"]},"client": client.web}))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass
		
	def sendMusic(self, guid, file_id , mime , dc_id,music_performer, time, access_hash_rec, file_name,  size , width , height, text=None, message_id=None):
		try:
			p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({"method":"sendMessage","input":{"object_guid":guid,"rnd":f"{randint(100000,900000)}","text":text,"reply_to_message_id":message_id,"file_inline":{"dc_id":str(dc_id),"file_id":str(file_id),"type":"Music","music_performer":music_performer,"file_name":file_name,"size":size,"time":time, "mime":mime, "access_hash_rec":access_hash_rec, 'width':width, 'height':height}},"client":{ client.android}}))},url=Bot.__getUrl__()).text)['data_enc']))
		except: pass
			
	def clearMessages(self, guid, message_ids):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"deleteMessages", "input":{ "object_guid":guid, "message_ids":message_ids,"type":"Global" }, "client": client.web }))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass
		
	def reciveUserInfo(self, guid):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getUserInfo", "input":{ "user_guid": guid }, "client": client.web }))},url=Bot.__getUrl__()).json()["data_enc"]))
		except: pass
		
	def reciveInfoByUsername(self, username): # user info without @
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getObjectByUsername", "input":{ "username":username }, "client": client.web }))},url=Bot.__getUrl__()).json().get("data_enc")))
		except: pass
		
	def reciveGroupAdmins(self, guid):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"client": client.web,
			"input":{
				"group_guid":guid
			},
			"method":"getGroupAdminMembers"
		}))},url=Bot.__getUrl__()).json().get("data_enc")))
		
	def reciveMessagesInfo(self, guid, message_ids):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getMessagesByID", "input":{ "object_guid": guid, "message_ids": message_ids }, "client":{ client.web}}))}, url=Bot.__getUrl__()).json()["data_enc"])).get("data").get("messages")
		except: pass

	def banMember(self, group_guid, user_guid):
		try:
			return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"banGroupMember", "input":{ "group_guid": group_guid, "member_guid": user_guid, "action":"Set" }, "client":{ client.web } }))},url=Bot.__getUrl__())
		except: pass

	def addGroupMembers(self, group_guid, user_guids):
		try:
			return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"addGroupMembers", "input":{ "group_guid": group_guid, "member_guids": user_guids }, "client":{ client.web } }))},url=Bot.__getUrl__())
		except: pass

	def setGroupDefaultAccess(self, group_guid, access_list):
		try:
			return post(json={ "api_version": "4", "auth": self.auth, "client": { client.android }, "data_enc": self.enc.encrypt(dumps({ "access_list": access_list, "group_guid": group_guid })), "method": "setGroupDefaultAccess" }, url=Bot.__getUrl__())
		except: pass

	def getMyStickerSets(self):
		try:
			return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({ "method":"getMyStickerSets", "input":{}, "client":{ client.web }}))},url=Bot.__getUrl__()).json().get("data_enc"))).get("data")
		except: pass

	def requestSendFile(self, name, size , mime):
		o = ''
		while str(o) != '<Response [200]>':
			o = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"requestSendFile",
				"input":{
					"file_name":name,
					"size":size,
					"mime":mime
				},
				"client":{
					"app_name":"Main",
					"app_version":"2.8.1",
					"platform":"Android",
					"package":"ir.resaneh1.iptv",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c66.iranlms.ir/")
			try:
				k = loads(self.enc.decrypt(o.json()["data_enc"]))
				if k['status_det'] == 'TOO_REQUESTS':
					return 'many_request'
				elif k['status'] != 'OK' or k['status_det'] != 'OK':
					o = '502'
			except:
				o = '502'
		return k['data']
		
	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Image",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'thumb_inline':thumb_inline,
										'width':width,
										'height':height
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url=Bot.__getUrl__()).text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url=Bot.__getUrl__()).text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url=Bot.__getUrl__()).text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url=Bot.__getUrl__()).text)['data_enc']))

	def fileUpload(self, bytef ,hash_send ,file_id ,url):		
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = round(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p

	def getThumbInline(self,image_bytes:bytes):
		im = Image.open(BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), Image.ANTIALIAS)
		changed_image = BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return b64encode(changed_image)
	
	@staticmethod
	def getImageSize(image_bytes:bytes):
		import io, PIL.Image
		im = PIL.Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return [width , height]
		
	def sendPhotoWithLink(self, guid, link, caption = None, msg_id = None):
		try:
			if caption != None and msg_id != None:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							try:
								access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
								self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption, msg_id)
							except: pass
				except: pass
			elif caption != None:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							try:
								access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
								self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption)
							except: pass
				except: pass
			elif msg_id != None:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							try:
								access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
								self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, msg_id)
							except: pass
				except: pass
			else:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							try:
								access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
								self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height)
							except: pass
				except: pass
		except: pass

	def sendPhoto(self, guid, file,caption =None, msg_id = None):
		try:
			if caption != None and msg_id != None:
				try:
					b2 = open(file,'rb').read()
					suffix = Path(file).suffix
					width, height = Bot.getImageSize(b2)
					tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
					if tx != 'many_request':
						try:
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption, msg_id)
						except: pass
				except: pass
			elif caption != None:
				try:
					b2 = open(file,'rb').read()
					suffix = Path(file).suffix
					width, height = Bot.getImageSize(b2)
					tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
					if tx != 'many_request':
						try:
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption)
						except: pass
				except: pass
			elif msg_id != None:
				try:
					b2 = open(file,'rb').read()
					suffix = Path(file).suffix
					width, height = Bot.getImageSize(b2)
					tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
					if tx != 'many_request':
						try:
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, msg_id)
						except: pass
				except: pass
			else:
				try:
					b2 = open(file,'rb').read()
					suffix = Path(file).suffix
					width, height = Bot.getImageSize(b2)
					tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
					if tx != 'many_request':
						try:
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendImage(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height)
						except: pass
				except: pass
		except: pass