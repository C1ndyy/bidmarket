# bidmarket
**Internet community auction house.**

The purpose of bidmarket is to buy and sell personal items by auction, over the internet.  Bid in real time bidding rooms, against other prospective buyers.  Sell your painting.  Sell your chair.  Sell your shoes.  Sell your collections.  Selling = more $$$.  Enough said.  Need something, but everyone is overcharging for it?  Buy it for what its really worth by auction with bidmarket.

# Table of contents
1. [Web app Link](#link)
2. [About Bidmarket](#about)
    1.  [Features](#features)
    2.  [Categories](#categories)

3. [Design and planning](#designandplanning)
    1. [Wireframes](#Wireframes)
    2. [Entity-Relationship Model](#ERD)
    3. [Github Projects](#trello)
4. [Contributors and Collaborators](#contributors)
5. [Technologies Used](#technology)
6. [Future Enhancements](#futureenhancement)

## Web app Link <a name="link"></a>
[Web app link here](https://bidmarket.herokuapp.com/)

## About Bidmarket <a name="about"></a>

This project was developed for educational purposes, and is a prototype.  This app allows the user to create, edit and delete listings(items), add photos to listings, and also search for listings posted and view them.  Upon viewing them the user is brought to a room with other users also bidding on an item.  A user can then place bids on the listing, updating the room dynamically.  A user can also message another user, for the purposes of enquiring about a listing.

As a Non-Authenticated User: 
- I want to be able to view all listings
- I want to search by keyword
- I want to sort by category
- I want to create an account via sign-up form

As a user: 
- I want to be able to log in
- I want to post items for bidding
- I want to edit and/or delete my listings
- I want to send and receive messages from other users in relation to the listed items
- I want to view all the items I have bid on


<img src="https://bitmarket-assets.s3.amazonaws.com/mobile-home.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/side-nav-mobile.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/website-details.png" height="300px" width="320px" >

### Features <a name="features"></a>
- Login and Sign up
- post items for bidding
- add/delete photos related to my items 
- update my items
- delete my items
- listing of all items (expired listings auto deleted from the list)
- Search by keyword
- Filter/sort by category, price, bid expiry date
- confirmations for bids, and deletes
- 8 preset increments for bid expiry date (3 hours, 24 hours, 3 days, 1 week, 2weeks, 1 month, 2 months, 3 months)
- messaging other users about posted items
- see my bid histroy and bid history on a particular item 

### Current categories on bidmarket <a name="categories"></a>
Currently there are five general categories for posting items: 
- Book
- Home
- Fashion
- Tech
- Sporting

More categories will be added in future enhancements

## Design and planning <a name="designandplanning"></a>

### Wireframes <a name="Wireframes"></a>
<img src="https://bitmarket-assets.s3.amazonaws.com/profile.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/details.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/detail-history.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/message.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/Search2.png" height="400px" width="200px" >
<img src="https://bitmarket-assets.s3.amazonaws.com/Search1.png" height="400px" width="200px" >

### Entity-Relationship Model <a name="ERD"></a>
<img src="https://bitmarket-assets.s3.amazonaws.com/bidmarket+ERD-v1.1.png" height="300px" width="320px" >

### Github Projects <a name="trello"></a>
Github Projects was used to organize and manage the our progress during our daily stands ups
[Github Projects]

## Contributors and Collaborators <a name="contributors"></a>
#### Designers (roles):
* [Charissa Ho] (Designer)
* [Quentin Caron] (Designer)
* [Roseanna Meas] (Designer)

#### Developers (roles):
* [Cindy Xu] (GitHub Manager, Project Liaison)
* [Robin Hylands] (Database manager)
* [Philip Cheung] (Scrum Master)

## Dev Tools Used <a name="technology"></a>
* HTML 5
* CSS 3
* Bootstrap 5
* Python 3.9
* Django 3.1.7
* Channels
* PostgreSQL
* AWS S3 storage
* Hosted on Heroku

## Future Enhancements <a name="futureenhancement"></a>
- implement a buy now price feature for users to buy an item immediately at an pre-determined price (by seller)
- live bidding on live version
- search by location, to view items being sold nearby
- creadit card and bitcoin payment method

[Charissa Ho]: https://www.linkedin.com/in/charissatho/
[Quentin Caron]: https://www.linkedin.com/in/q-caron/
[Roseanna Meas]: https://www.linkedin.com/in/roseannajm/
[Cindy Xu]: https://github.com/C1ndyy
[Robin Hylands]: https://github.com/robin10125
[Philip Cheung]: https://github.com/pdccheung
[Github Projects]: https://github.com/C1ndyy/bidmarket/projects/1



