import requests
import csv

# creating universal class for dynamic sites
class Connect:

	def __init__(self, url):
		self.headers = {
			'user-agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
		}
		self.response = requests.get(url, headers=self.headers)
		

	def return_page(self):
		return self.response.json()


def parse_pages():
	# we cant know number of pages, that`s why we have to check product id
	page_exists = True
	page_number = 1
	products = []
	products_ids = []

	while page_exists:
		try:
			# connecting
			url = f'https://wbxcatalog-ru.wildberries.ru/men_clothes/catalog?spp=0&regions=79,64,40,68,4,38,30,33,70,1,22,31,66,80,48,69&stores=119261,122252,122256,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,124583,124584,117986,1733,116433,120762,119400,117501,507,3158,2737,1699,686,1193,117413,119781&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=2,12,6,7,3,21&kind=1;11&subject=153&sort=popular&page={page_number}'
			connect = Connect(url)
			page_text = connect.return_page()

			# getting product data from request
			for product in page_text['data']['products']:
				product_id = product['id']
				product_brand = product['brand']
				product_price = int(product['salePriceU']) / 100

				# checking if product_id is already parsed
				if product_id in products_ids:
					page_exists = False
				else:
					products_ids.append(product_id)

				products.append(
					{
					'Id' : product_id,
					'Brand' : product_brand,
					'Price' : product_price
					}
				)
				
			print(f'[INFO] Page {page_number}')
			page_number += 1
		except:
			page_exists = False

	return products

def main():
	# creating headers
	with open('data.csv', 'w', newline = '', encoding='utf-8') as file:
		writer = csv.writer(file, delimiter=' ')
		writer.writerow(
			(
				'Product type',
				'Product brand',
				'Product price'
			)
		)
	# adding information to excel
	products = parse_pages()
	with open('data.csv', 'a', newline='') as file:
		writer = csv.writer(file, delimiter = ' ')
		for product in products:
			writer.writerow(
				(
					product['Id'],
					product['Brand'],
					product['Price']
				)
			)
	
if __name__ == '__main__':
	main()