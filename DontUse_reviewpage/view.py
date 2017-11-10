from flask import Flask, render_template, flash, redirect
from app import app
import math

@app.route("/review")
@app.route("/reviewpage")
@app.route("/REVIEW")
@app.route("/REVIEWPAGE")

def index():
