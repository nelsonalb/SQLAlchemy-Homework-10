# sqlalchemy-challenge
Module 10 SQL Challenge

## Instructions
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

* Part 1: Analyze and Explore the Climate Data.

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.

Use the SQLAlchemy create_engine() function to connect to your SQLite database.

Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.

Link Python to the database by creating a SQLAlchemy session.

Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

* Part 2: Design a Climate App.

## Part 1: Analyze and Explore the Climate Data
In this section, I used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib.
* Precipitation Analysis
   - Found the most recent date in the dataset 
   - Using that date, got the previous 12 months of precipitation data by querying the previous 12 months of data
   - Selected only the "date" and "prcp" values
   - Loaded the query results into a Pandas DataFrame, and set the index to the "date" column
   - Sorted the DataFrame values by "date"
   - Plotted the results.
   - Used Pandas to print the summary statistics for the precipitation data.
* Station Analysis
   - Designed a query to calculate the total number of stations in the dataset
   - Designed a query to find the most-active stations, listing the stations and observations in descending order and answering which station id had the greatest number of obervations
   - Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query
   - Designed a query to get the previous 12 months of temperature observation (TOBS) data
   - Plotted the results.
   
## Part 2: Design a Climate App
In this section, I designed a Flask API based on the previous queries. 

Included are:
* Precipitation Route
   - Shows the preceiptation data for the last year in the database
   - Returns json with the date as the key and value as the precipitation
* Stations Route
   - Shows a list of all weather stations in database
   - Returns jsonified data 
* Tobs Route
   - Shows the last year of data for the most active station
   - Returns jsonified data 
* Dynamic Routes Allowing User to Enter Start and/or End Dates
   - Allows user to enter their own start date to see minimum, average and maximum temperatures after that date
   - Allows user to enter their own start and end date to see minimum, average and maximum temperatures between those dates
