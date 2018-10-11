from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import requests
import xlsxwriter as xl
def init():
	driver = webdriver.Chrome(executable_path='D:\\Python\\Project needs\\chromedriver.exe')
	driver.get("http://www.amazon.ca")
	return driver

def searchTab(driver):
	search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
	search.send_keys(input("What do u want to search ? "))
	botton = driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
	botton.click()
	return driver

def searchWaitResult(driver):
	my_url = driver.current_url
	return my_url

def start_webscraping(my_url):
	col=['Product','Inventory','Reviews']
	Table=[]
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
	res = requests.get(my_url, headers=headers)
	res.raise_for_status()
	page_soup = soup(res.text,"html.parser")
	Total = page_soup.findAll("div",{"class":"s-item-container"})
	max=len(Total)
	n=int(input('how many results are we looking for (no longer than '+ str(max)+ ' )?'))
	container = []
	for i in range (n):
		List=[]
		id = "result_"+str(i)
		box = page_soup.findAll("li",{"id":id})[0]
		container.append(box)
		# now we have all the info we want
		product = box.findAll("h2")[0]
		product = product.get_text()
		List.append(product)
		stock = box.findAll("span",{"class":"a-size-small a-color-price"})
		if stock:
			stock = stock[0].get_text
			invent1,invent2 = str(stock).split('Only ')
			invent3,invent4 =invent2.split(' left')
			List.append(invent3)
		else:
			List.append("plenty")
		review = box.findAll("a",{"class":"a-size-small a-link-normal a-text-normal"})
		if review:
			review=review[0]
			review=str(review)
			if 'CDN' in review:
				review2=review.split('CDN$ ')
				review3=review2[1].split('<')
			else:
				review1=review.split('>',2)
				review3=review1[1].split('<')
			List.append(review3[0])
		else:
			List.append("Nuh")
		Table.append(List)
	Final=pd.DataFrame(Table,columns=col)
	return Final

def export_to_excel(table):
	# wb=xl.Workbook("Amazon.xlsx")
	# worksheet  =wb.add_worksheet()
	writer = pd.ExcelWriter('Amazon.xlsx',engine='xlsxwriter')
	Workbook=writer.book
	table.to_excel(writer,sheet_name='Amazon')
	worksheet=writer.sheets['Amazon']
	writer.save()
	# wb=writer.book
	# ws=writer.sheets['Amazon']



if __name__ == '__main__':
	driver = init()
	driver=searchTab(driver)
	result_url = searchWaitResult(driver)
	table = start_webscraping(result_url)
	print (table)
	export_to_excel(table)






