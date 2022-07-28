import scrapy, logging, yaml, os
from scrapy.crawler import CrawlerProcess
from colorama import Fore, Style

class cryptoCalculator():
	def __init__(self):
		self.configFile = 'crypto-config-example.yml'
		self.clearScreen = True # Do not clear screen, print error codes. Debug tool.

	def yamlLoad(self): # Load yaml passed as param
		with open(self.configFile, 'r') as r:
			yl = yaml.safe_load(r)
			return yl

	def yamlDump(self, newYaml):
		with open(self.configFile, 'w') as w:
			yaml.dump(newYaml, w)

	def get(self, keys, yawn): # Try/Except function for loading values from yaml/json passed as parameter.
		try:
			if not isinstance(keys, list): # If parameter is not list (single string)
				keys = [keys] # turn into a list

			nest = ''
			for key in keys:
				try:
					key = int(key)
					nest += f'[{key}]'
				except:
					nest += f'["{key}"]'

			lessNest = eval(f'yawn{nest}')
			return lessNest

		except Exception as e:
			print(f'Error in get(): {e}')

	def printConfig(self): # Pretty Print and Calculations for various crypto investments
		def clearScreen():
			if os.name == 'nt': # Clear stdout if on windows
				os.system('cls')
			else: # [Likely] being used on android w/ pydroid app
				os.system('clear')

		if self.clearScreen == True:
			clearScreen()
		else:
			pass
		
		yl = self.yamlLoad() # load default yaml file
		xy = '-' * 65 # total length of ppretty print border

		print(xy)
		print ("| {:<6} | {:<7} | {:<7} | {:<7} | {:<9} | {:<10} |".format('Symbol', 'Ticker', '24HR', 'Asset', 'Liability', 'Loss/Gain')) # headers
		print(xy)

		for coin in yl:
			if coin != 'total': # Recusively perform below operations for all coins in yml
				ticker = float(self.get([coin, 'ticker', 'price'], yl))# Stock ticker of coin from last scrape
				daytic = self.get([coin, 'ticker', '24HR'], yl)
				asset = self.get([coin, 'asset'], yl) # Asset Value of investments
				symbol = self.get([coin, 'symbol'], yl) # Coin's symbol
				invest = self.get([coin, 'invested'], yl) # Total investments into coin
				lossGain = round(asset - invest, 2)
	
				daytic = [Fore.GREEN + str(daytic) if '+' in daytic else Fore.RED + str(daytic)][0] + Fore.WHITE
				lossGain = [Fore.GREEN + str(lossGain) if lossGain >= 0 else Fore.RED + str(lossGain)][0] + Fore.WHITE
				# ^ if gains >= 0 print highlight text green else highlight red
				tic, daytic, ast, inv, log = [f'{ticker}', f'{daytic}', f'{asset}', f'{invest}', f'{lossGain}']
				print("| {:<6} | {:<7} | {:<17} | {:<7} | {:<9} | {:>20} |".format(symbol, tic, daytic, ast, inv, log))
	
		cost = self.get(['total', 'cost'], yl)
		costStr = f"Spent: {round(cost, 2)}"

		value = self.get(['total', 'value'], yl)
		valStr = f"Value: {round(value, 2)}"
	
		mar = round(value / cost * 100, 2)
		mar = [Fore.RED + str(mar) if mar < 100 else Fore.GREEN + str(mar)][0] + Fore.WHITE
		# ^ If margin is less than 100% of investment, print red. elsif > 100% print green ^
		marginStr = f"Margin: {mar}"
		cosValMar = "| {:^17} | {:^22} | {:^26} |".format(costStr, valStr, marginStr)

		print(f'{xy}\n{cosValMar}\n{xy}') # pretty print border and config/scraped balances

class CryptoSpider(scrapy.Spider):
	name = 'crypto'
	start_urls = ['https://crypto.com/price/']
	handle_httpstatus_list = [404]
	logging.getLogger('scrapy').propagate = False

	def __init__(self):
		crycal = cryptoCalculator()
		self.crycal = cryptoCalculator()
		self.yl = crycal.yamlLoad() # Load yaml config
		self.yl['total']['value'] = 0 # Reset yaml grand totals, to be determined by next scrape
		self.yl['total']['cost'] = 0 # Reset yaml grand totals, to be determined by next scrape

		self.coins = [yam for yam in self.yl if yam != 'total'] # Return each token name (key) in yaml as long as it's not 'total'

	def start_requests(self): # Scrape various info for each token name in yaml file
		urls = [f'https://crypto.com/price/{suffix}' for suffix in self.coins]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.recursiveParse)

	def recursiveParse(self, response): 
		for stat in response.xpath('//div[@class="css-13lnf1p"]'):
			if response.status != 404:
				symbol = stat.xpath('//h1[@class="chakra-heading css-d45eer"]/text()').get() # XPATH to scrape token symbol
				coin = response.url.split('/')[-1]
				price = stat.xpath('//span[@class="chakra-text css-13hqrwd"]/text()').get() # XPATH for current stonk price
				price = price.replace(' USD', '').replace('$', '').replace(',', '')
				price = round(float(price), 5)

				dayTicker = response.xpath('//p[@class="chakra-text css-1vqnh5f"]/text()').get() # Dayticker is positive
				if dayTicker == None: # Dayticker is not positive, negative is under a different xpath
					dayTicker = response.xpath('//p[@class="chakra-text css-v338os"]/text()').get() # Get negative dayticker
				dayTicker = str(dayTicker)

				yamlCoin = self.yl[coin] 
				yamlCoin['symbol'] = symbol # Update yaml
				satoshi = yamlCoin['satoshi'] # To be used for calculating new value of tokens
				yamlCoin['ticker']['price'] = price # Update yaml ticker value
				yamlCoin['ticker']['24HR'] = dayTicker

				coinInvestment = 0 # Place holder for incremental counter
				satoshiTotal = 0
				for date in yamlCoin['purchases']:
					for purchase in yamlCoin['purchases'][date]:
						if '$' in purchase:
							purchase = round(float(purchase.replace('$', '')), 2)
							coinInvestment += purchase # Yaml key value will not round if += directly
							yamlCoin['invested'] = coinInvestment # Update yaml invested value with rounded subtotal
							self.yl['total']['cost'] += purchase # Update total sunk cost based on any token purchases in yaml config
						elif yamlCoin['symbol'] in purchase:
							purchase = purchase.replace(yamlCoin['symbol'], '')
							satoshiTotal += float(purchase)
							yamlCoin['satoshi'] = satoshiTotal
			else:
				print(response.status, response.url) # There was an error with scraping a specific token

			asset = round(float(price) * satoshi, 2)
			yamlCoin['asset'] = asset
			self.yl['total']['value'] += asset

		self.crycal.yamlDump(self.yl) # Dump yaml of updated key/values

if __name__ == "__main__":
	process = CrawlerProcess()
	process.crawl(CryptoSpider)
	process.start()
	calc = cryptoCalculator()
	calc.printConfig()