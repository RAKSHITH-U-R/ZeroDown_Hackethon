# ZeroDown_Hackethon

## Introduction
Housing market in the US relies heavily on supply and demand. The buyer places an offer to
buy a home, leaving the seller to accept or reject the offer. For example, if a market has a high
demand and low supply in housing stock, owners often benefit from getting a higher price for
their homes. But if there are a ton of properties for sale and only a few buyers, the sellers may
end up getting less than their asking price.

## objectives
Come up with a score that indicates the hotness of a given market i.e., how difficult it is to win a
home in an area. By being able to compare the level of competition in different areas, customers
can hone in on neighborhoods where they’re more likely to place a successful offer.

## Milestones
1. Import data into a database
2. Define an algorithm to determine the score of a given market
3. Create a simple UI that takes market id as input and returns the formulated score
4. Add insights/visualizations that justifies your approach for computing the score

## Approach

```hotness_score = (sold_homes_count / new_listings_count) * (homes_sold_over_list_price_count / sold_homes_count) * (1 - (median_sale_to_list_ratio)) * (1 / days_to_sell)```
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

## Backend Routes (API routes)

https://market-rakshith-u-r.vercel.app/market?market_id="market_id"

example: https://market-rakshith-u-r.vercel.app/market?market_id=15663

above api is used to get the score of the market_id entered by the user.

https://market-rakshith-u-r.vercel.app/all

above api is used to get Scores of all the markets present in the database.

https://market-rakshith-u-r.vercel.app/top5

above api is used to get top 5 markets with highest score.

https://market-rakshith-u-r.vercel.app/history

above api is used to fetch history of the market over the years

## Frontend Hosting
Frontend is hosted in Vercel : https://market-gui.vercel.app

No problems were faced in hosting the frontend.

## Frountend Routes

https://market-gui.vercel.app/

Above links renders a page where user can enter the market id and get the score of the market.

Udated this link to display teh trend of the market over the year

https://market-gui.vercel.app/stats

Above links renders a page where user can see the plots.

Due to some error the plots are not rendering properly. I am working on it.

Fixed the error now abel to plot bar plot for top 5 markets