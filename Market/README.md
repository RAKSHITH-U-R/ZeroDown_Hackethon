# Approach

hotness_score = (sold_homes_count / new_listings_count) * (homes_sold_over_list_price_count / sold_homes_count) * (1 - (median_sale_to_list_ratio)) * (1 / days_to_sell)
The idea behind this calculation is that a market with a high "hotness score" would have:

1. A high number of sold homes compared to new listings, indicating high demand
2. A high percentage of homes sold above the list price, indicating strong competition and bidding wars
3. A low median sale to list ratio, indicating that homes are selling for close to or above the list price
4. A short time to sell, indicating that homes are quickly being snapped up by buyers

## Backend Hosting
Backend is hosted in Vercel : https://market-rakshith-u-r.vercel.app/market?market_id=15663

Problems faced:
1.  Fist problem Faced was in connecting to the Database which was local. So i hosted the database in elephantSQL and connected to it.
2.  Initially i used to fetch data from the Database everytime the user enters the market id and calculate the Score. But this was taking a lot of time to respond back to server. which lead to timeout error.So i decided to calculate the score once and store it in another Table. Next time when the user enters the market id, the score is fetched from the table instead of calculating it again.

## backend Routes (API routes)

https://market-rakshith-u-r.vercel.app/market?market_id="market_id"

example: https://market-rakshith-u-r.vercel.app/market?market_id=15663

above api is used to get the score of the market_id entered by the user.

https://market-rakshith-u-r.vercel.app/all

above api is used to get Scores of all the markets present in the database.