from flask import Flask, render_template, flash, redirect, request, url_for
from app import app, db, data
from app.models import Apartment, Address, City, Review
from app.forms import SearchForm, ReviewForm
import math, datetime

# Home page
@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = SearchForm()
    # when provided a valid search, redirect to filter page
    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for('filter', search=search))
    return render_template('home.html', title="Rate My Apartment", form=form)


# Filter page
@app.route('/filter/<search>', methods=['GET', 'POST'])
def filter(search=None):
    form = SearchForm()
    # Search for the city
    search = search.capitalize()
    if search is not None:
        city = db.session.query(City).filter(City.name == search).one_or_none()
        if city == None:
            apartments = []
        else:
            apartments = city.apartments
    # define helper functions that will be used in the page
    def length(a):
        return len(a)
    def rounD(a):
        return round(a)
    def string(a):
        return str(a)
    # when search again, redirect back to this page with the new search keyword
    if form.validate_on_submit():
        search = form.search.data
        return redirect(url_for('filter', search=search))
    return render_template('index.html', title='Search ' + search, \
                            apartments=apartments, \
                            rows=math.ceil(len(apartments) / 3),\
                            length=len(apartments), \
                            len=length, form=form,int=rounD,\
                            str=string)

# Review page
# take in zpid as parameter
@app.route('/reviewpage/<int:zpid>', methods=['GET', 'POST'])
def reviewpage(zpid, submitted=False):
    # query the databse for this apartment
    this_apart = db.session.query(Apartment).filter(Apartment.zpid == zpid).one_or_none()
    form = ReviewForm()
    # when a review is submitted
    if form.validate_on_submit():
        # store this review, and add this rating score to the apartment's overall
        username = form.username.data
        rating = int(form.rating.data)
        content = form.content.data
        timestamp = datetime.date.today()
        new_review = Review(user_name=username, content=content, rating=rating, time_stamp=timestamp)
        this_apart.average_rating = (this_apart.average_rating * this_apart.review_number + rating) / (this_apart.review_number + 1)
        this_apart.review_number += 1
        this_apart.review.append(new_review)
        db.session.commit()
        flash('Thank you for submitting your comments!')
        return redirect(url_for('reviewpage', zpid=zpid, submitted=True))
    # define helper function for this page
    def length(a):
        return len(a)
    def rounD(a):
        return round(a)
    def string(a):
        return str(a)
    return render_template('reviewpage.html', title=this_apart.address[0].street, \
                                              apartment=this_apart, \
                                              len=length,\
                                              int=rounD,\
                                              str=string,\
                                              form=form,\
                                              submitted=submitted)


app.secret_key = 'CS196'
