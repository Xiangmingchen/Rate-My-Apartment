CS196 Project - Rate My Apartment

![alt text] (https://github.com/CS196Illinois/Rate-My-Apartment/blob/master/images/landing%20page.png)

Project Contributor: Yiyin Shen, Siyuan Teng, Xiangming Chen, Rick Iwanaga
Project Manager(Mentor): Anna B.

Please check out the descriptions below to understand: 1. What we did, 2. What We can do through the product(web app) 
& 3 what we can do in the future to improve the product.

1 What we've done:

    Front-end (created) :
      -We used HTML, CSS, and Bootstrap for: 
        >Home page (Landing page) 
        >List page of apartments in a selected city
            >>Apartment location, price & rating
        >Review page of apartment 
            >>Used Js to implement slideshow of apartment pictures
            >>Used Js to capture star rating
            >>Used Google Map API to display apartment location 

    Back-end (used/did):
      -ZillowAPI to pull data of existing apartments in Illinois (https://www.zillow.com/howto/api/APIOverview.htm)
      
      -SQLAlchemy to store the data of apartments and their reviews 
      
      -Flask WTF to create a review form on review page
          >data collected from the form is stored in SQLAlchemy
          
      -ElementTree to parse the response from ZillowAPI

2 What we can do through the web app:

    -Search apartments in Illinois by location(city) filter.
    
    -Check details of apartments in Illinois (i.e. Champaign, Urbana)
        >Photos of apartments, rooms, amenities, location (Google Map), ratings (5 stars) & reviews
        
    -Upload review of apartments through review page
        >Name, rating, & review details are stored
        
![alt text]  (https://github.com/CS196Illinois/Rate-My-Apartment/blob/master/images/listing.png)
![alt text]  (https://github.com/CS196Illinois/Rate-My-Apartment/blob/master/images/reviewpage.png)

3 What we can improve:

    -By using Zillow API , we can add more cities/states. We did not add cities from other states to prevent 
    potential issues like duplicate city name in other state(s).

    -Use Google Authentication for user login/signup as it provides better/robust security. 

    -List apartments from more than 2 cities for better user-experience.

    -Add variety of filter functions such as price, rating, reviews, amenities and roommates.

    -Add pagination so that cities with large amount of apartments will load faster
