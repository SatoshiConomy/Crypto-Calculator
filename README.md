# Crypto-Calculator
 Scrapes coin values, calculates investments, monitors block explorer balances and pretty prints to command line. <br>
 Runs on PyDroid3 App for Android and/or Windows cmd.

<img src="https://github.com/SatoshiConomy/Crypto-Calculator/blob/main/example-cli-output.png?raw=true" width=65% height=65%>
<img src="https://github.com/SatoshiConomy/Crypto-Calculator/blob/main/pydroid.jpg?raw=true" width=65% height=65%>

*These are example pictures made from random yaml configs, meant only to illustrate*

The aim of the game is to make investments but own your coin. Exchanges are great for purchasing and selling quickly but not for security. (Custodial hot wallet) So put your coin in a non custodial, cold wallet but then how do you monitor it? An exchange can no longer tell you what your coin/investment is valued at.

Crypto-Calculator solves both of these. If you have crypto in multiple places, this allows you to monitor offline wallets through Blockchain Explorers while getting insights on tokens currently on an exchange. It's quicker than using Crypto.com's interface especially when you just want a quick snapshot of the market. It's arguably more secure since it would mean accessing sensitive exchange apps fewer times or exposing less pin numbers.

## Why
- Quicker than manually checking market on Crypto.com app installed in encrypted folder behind 3 passwords.
- Provides more win/loss insights than one [inflated*] total number in Crypto.com app
- Monitor offline wallets, not available in exchanges, by scraping blockchain explorers

\**Inflated because if you have any CRONOS (worthless/locked referal incentives) then your gains/losses aren't accurate to actual purchases*

## Yaml Config Information and Example

```yaml
apecoin-ape: # Token name as it appears in Exchange site url, to be scraped. ie: www.crypto.com/price/{X} (manual)
  asset: # Total asset calculated from information provided below (auto)
  invested: 1 # Subtotal of any string under 'purchases' containing '$' character - Value A - (auto)
  purchases: # List of purchases
    3.26.22: # Date of purchase (manual)
    - $0.99 # Amount purchased - Value A - (manual)
    - 1 APE # Tokens purchased - Value B - (manual)
    - '@24.99' # Value of token at time of purchase (manual) # Unused and Uneeded
  satoshi: 0.99 # Total satoshi of values in purchases matching crypto symbol - Value B - (auto)
  symbol: APE # Scraped currency symbol (auto)
  ticker:
   24HR: -2.80% # 24 hour stonk fluctuation (auto)
   price: '4.59' # current stonk price (auto)
ethereum:
  asset:
  invested:
  purchases:
  satoshi:
  symbol:
  ticker:
filecoin:
  asset:
  invested:
  purchases:
  satoshi:
  symbol:
  ticker:
total:
  cost: 1 # Total cost of investments (auto)
  value: # Total current valuation of investments (auto)
```

## TODO
- <strike>Get total 'satoshi' value in yaml config from manual 'purchases' info</strike>
- <strike>Get coin 'invested' value in yaml config from manual 'purchases' info</strike>
- <strike>After these have been added, manual array in 'purchases' needs only be len() of 2 instead of 3</strike>
- Expand x.get(y, yaml) method out to be used in Spider Class
