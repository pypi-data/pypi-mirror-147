from rubika_lib.lib import Bot
from random import randint
from requests import get
from pathlib import Path

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
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendPhoto(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption, msg_id)
				except: pass
			elif caption != None:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendPhoto(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption)
				except: pass
			elif msg_id != None:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendPhoto(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, msg_id)
				except: pass
			else:
				try:
					res = get(link)
					if res.status_code == 200 and res.content != b'':
						b2 = res.content
						width, height = Bot.getImageSize(b2)
						tx = self.requestSendFile("tg" + str(randint(1000000, 9999999)) + '.png', len(b2), 'png')
						if tx != 'many_request':
							access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
							self.sendPhoto(guid ,tx['id'] , 'png', tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height)
				except: pass
		except: pass
def _sendPhoto(self, guid, file ,caption = None, msg_id = None):
	try:
		if caption != None and msg_id != None:
			try:
				b2 = open(file,'rb').read()
				width, height = Bot.getImageSize(b2)
				tx = self.requestSendFile("rubika_library"+str(randint(1000,9999)), len(b2), 'png')
				if tx != 'many_request':
					access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
					self.sendPhoto(guid ,tx['id'] , "png", tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption, msg_id)
			except: pass
		elif caption != None:
			try:
				b2 = open(file,'rb').read()
				width, height = Bot.getImageSize(b2)
				tx = self.requestSendFile("rubika_library"+str(randint(1000,9999)), len(b2), "png")
				if tx != 'many_request':
					access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
					self.sendPhoto(guid ,tx['id'] , "png", tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, caption)
			except: pass
		elif msg_id != None:
			try:
				b2 = open(file,'rb').read()
				width, height = Bot.getImageSize(b2)
				tx = self.requestSendFile("rubika_library"+str(randint(1000,9999)), len(b2), "png")
				if tx != 'many_request':
					access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
					self.sendPhoto(guid ,tx['id'] , "png", tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height, msg_id)
			except: pass
		else:
			try:
				b2 = open(file,'rb').read()
				width, height = Bot.getImageSize(b2)
				tx = self.requestSendFile("rubika_library"+str(randint(1000,9999)), len(b2), "png")
				if tx != 'many_request':
					access = self.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
					self.sendPhoto(guid ,tx['id'] , "png", tx['dc_id'] , access, 'tg'+ str(randint(1000000, 9999999)) + '.png', len(b2), str(self.getThumbInline(b2))[2:-1] , width, height)
			except: pass
	except: pass