import json
import os
import requests
import toolz
import click

from typing import Dict, Any
from .exceptions import PurifyFormatException


@click.group()
def cli():
    pass


def _webPurifyRequest(url: str, apiKey, method: str, query: Dict[str, Any]) -> Dict[str, Any]:
	query = toolz.merge({
		'method': method,
		'api_key': apiKey,
		'format': 'json',
	}, query)
	response = requests.post(url, data = query)
	response.raise_for_status()
	data = response.json()
	if 'err' in data['rsp']:
		raise PurifyFormatException(
			data['rsp']['err']['@attributes']['msg'], 
			code = data['rsp']['err']['@attributes']['code']
		)
	return data['rsp']

@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--text', help='text to check profanity', required=True)
@click.option('--lang', default='en', help='language of the text')
def checkText(token: str, text: str, lang: str) -> bool:
	'''
	This function should be used to check a string or sentence for profanity, if profanity is 
	found 'True' is returned, else 'False' is returned.  This function will not return the number of words detected,
	just the fact they have been detected.
	For more info see: https://www.webpurify.com/documentation/methods/check/
	'''
	response = _webPurifyRequest('http://api1.webpurify.com/services/rest/', token, 'webpurify.live.check', {
		'text': text,
		'lang': lang    
	})
	print(response['found'] == '1')


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--text', help='text to check profanity', required=True)
@click.option('--lang', default='en', help='language of the text')
def replaceText(token: str, text:str, lang: str, replaceSymbol='*'):
	'''
	This function is used to replace profanity in the text with * 
	'''
	response = _webPurifyRequest('http://api1.webpurify.com/services/rest/', token, 'webpurify.live.replace', {
		'text': text,
		'lang': lang,
		'replacesymbol': replaceSymbol   
	})
	if response['found'] > '0':
		return response['text']
	print(text)


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--image-url', help='text to check profanity', required=True)
def checkImage(token: str, image_url: str, purifyMethod = 'webpurify.live.imgcheck') -> str:
	'''
	This fuction submits an image to the checked for profanity, it returns a uniqe image ID that
	needs to be used to poll the webPurify servers for a image review status.
	To test the api pass 'purifyMethod=webpurify.sandbox.imgcheck', this will bypass the actual profanity check
	for more info see: https://www.webpurify.com/image-moderation/documentation/methods/imgcheck/
	'''	
	response = _webPurifyRequest('http://im-api1.webpurify.com/services/rest/', token, purifyMethod, {
		'imgurl': image_url    
	})
	print(response['imgid'])

@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--image-url', help='image id to check the status', required=True)
def checkNudityInImage(token: str, image_url: str, purifyMethod = 'webpurify.aim.imgcheck') -> str:
	'''
	This function checks the % of nudity in an image
	'''
	response = _webPurifyRequest('http://im-api1.webpurify.com/services/rest/', token, purifyMethod, {
		'imgurl': image_url    
	})
	print(float(response['nudity']))


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--image-id', help='image id to check the status', required=True)
def checkImageStatus(token: str, image_id: str, purifyMethod = 'webpurify.live.imgstatus') -> str:
	'''
	This fuction should be used to poll the webPurify servers for the status of a 'checkImage' call.
	possible responses are pending, approved, declined.
	Use To test the api pass 'purifyMethod=webpurify.sandbox.imgstatus', if that was used in the checkImage call.
	for more info see: https://www.webpurify.com/image-moderation/documentation/methods/imgstatus/
	'''
	response = _webPurifyRequest('http://im-api1.webpurify.com/services/rest/', token, purifyMethod, {
		'imgid': image_id    
	})
	print(response['status'])


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--word', help='word to add into blacklist', required=True)
def addWordToBlackList(token: str, word: str) -> bool:
	'''
	This function is used to add a word to the set of words used to check for profanity, words in this list
	will be flaged in the checkText call.  NOTE: all language calls will search this list.
	For more info see: https://www.webpurify.com/documentation/methods/addtoblacklist/
	'''
	response = _webPurifyRequest('http://api1.webpurify.com/services/rest/', token, 'webpurify.live.addtoblacklist', {
		'word':word,  
	})
	print(response['success'] == '1')


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--word', help='word to remove from blacklist', required=True)
def removeWordFromBlackList(token: str, word: str) -> bool:
	'''
	This fuction removes a word added either through the webPurify website of the addWordToBlackList.
	for more info see: https://www.webpurify.com/documentation/methods/removefromblacklist/
	'''
	response = _webPurifyRequest('http://api1.webpurify.com/services/rest/', token, 'webpurify.live.removefromblacklist', {
		'word':word,  
	})
	print(response['success'] == '1')


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--word', help='word to add into whitelist', required=True)
def addWordToWhiteList(token: str, word: str) -> bool:
	'''
	This function adds a word to an 'allowed' list that is currently flagged by the standard webPurify list as containing 
	profanity.
	for more info see: https://www.webpurify.com/documentation/methods/addtowhitelist/
	'''
	response = _webPurifyRequest('http://api1.webpurify.com/services/rest/', token, 'webpurify.live.addtowhitelist', {
		'word':word,  
	})
	print(response['success'] == '1')


@cli.command()
@click.option('--token', help='WEBPURIFY_API_TEXT_KEY', required=True)
@click.option('--word', help='word to remove from whitelist', required=True)
def removeWordFromWhiteList(token: str, word: str) -> bool:
	'''
	This function removes a word to an 'allowed' list that is currently flagged by the standard webPurify list as containing 
	profanity.
	for more info see: https://www.webpurify.com/documentation/methods/removefromwhitelist/
	'''
	response = _webPurifyRequest('http://api1.webpurify.com/services/rest/', token, 'webpurify.live.removefromwhitelist', {
		'word':word,  
	})
	print(response['success'] == '1')
