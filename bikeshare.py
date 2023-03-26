"""
 used websites with good help for syntax/ functions:
    - https://pandas.pydata.org/docs/
        - https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
    - https://www.w3schools.com/python/pandas/default.asp
    - content from udacity
    - https://www.learnpython.org/
"""

import time
import pandas as pd
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

FILTER_OPTION_DATA = ['month', 'weekday', 'both', 'none']

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all' ]



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    """get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs"""

    city = ''
    
    while city.lower() not in CITY_DATA:
        city = input("\nWhich city should be analysed? Please choose one of the following cities: chicago, new york city, washington)\n").lower()
        if city in CITY_DATA:
            print("\nThanks, we will continue the analysis with the city " + city + ".")
            
        else:
            """Cityname is not in the list, repeating the loop necessary."""
            print("\nSorry, we cannot find your input of city " + city + " in the list of cities. Please choose one of the following cities: chicago, new york city, washington)\n\n")

    """what should be filtered? ask for userinput"""
    filteroptions = ''
    while filteroptions.lower() not in FILTER_OPTION_DATA:
        filteroptions = input("\nBased on which criteria do you want to filter? Month, weekday, both or non of them? Please choose one of the following options: month, weekday, both, none.\n")
        if filteroptions.lower() in FILTER_OPTION_DATA:
            if filteroptions == 'none':
                print("\nThanks, we will continue without filtering for month or weekday.")
            else:
                print("\nThanks, we will now continue asking for the specific filter options.")
        else:
            print("\nSorry, we cannot find your input of the filteroptions " + filteroptions + " in the referencelist. Please choose one of the following options: month, weekday, both, none\n\n")


    month = ''
    day = ''

    """based on the question what should be filtered, ask for month/ weekday/ nothing (=set month + day = all)"""
    if filteroptions.lower() in ['both', 'month']:
        """ get user input for month (all, january, february, ... , june). Include all, so the user can chose all month even if he said he wanted to filter..."""
        
        while month.lower() not in MONTH_DATA:
            month = input("\nWhich month should be analysed? Please choose one of the following months: january, february, march, april, may, june or all.\n").lower()
            if month.lower() in MONTH_DATA:
                if month == 'all':
                    print("\nThanks, we will not filter for a specific month and continue the analysis including all months.")
                else:
                    print("\nThanks, we will continue the analysis with the month " + month + ".")
            else:
                """Month is not in the list, repeating the loop."""
                print("\nSorry, we cannot find your input of month " + month + " in the list of months. Please choose one of the following months: january, february, march, april, may, june or all.)\n\n")
    
    if filteroptions.lower() in ['both', 'weekday']:
        """ get user input for day of week (all, monday, tuesday, ... sunday). Include all, so the user can chose all weekdays even if he said he wanted to filter..."""
        while day.lower() not in DAY_DATA:
            day = input("\nWhich day should be analysed? Please choose one of the weekdays or write all, if you want to continue analysing all days.\n").lower()
            if day in DAY_DATA:
                if day == 'all':
                    print("\nThanks, we will not filter for a specific day and continue the analysis including all days.")
                else:
                    print("\nThanks, we will continue the analysis with the day " + day + ".")
            else:
                """day is not in the list, repeating the loop."""
                print("\nSorry, we cannot find your input of day " + day + " in the list of days. Please choose one of the following inputs: monday, tuesday, wednesday, thursday, friday, saturday, sunday or all.)\n\n")
    
    if filteroptions.lower() == 'weekday':
        month = 'all'
        
    if filteroptions.lower() == 'month':
        day = 'all'
    
    if filteroptions.lower() == 'none':
        """request for filter options, based on previous input; set all, in case "none" was choosen, this is used (no specific if needed)"""
        month = 'all'
        day = 'all'


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    """load data file of the city that was choosen"""
    df = pd.read_csv(CITY_DATA.get(city))
    
    """# Missing columns to apply the filters: Month of starttime, weekday of starttime, Starthour (used for counting later on)"""

    """ monthname, weekday, Starthour, to do so start time has to be converted to datetime first"""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    """ if not 'all' was entered for month, then filter for monthname"""
    if month != 'all':
        """ modify monthname to month number, to be able to use integer instead of string for further calculations"""
        month_int = MONTH_DATA.index(month)
        """ filter by month to create the new filtered dataframe"""
        df = df[df['month'] == month_int]

    if day != 'all':
        """ filter by day of week to create the new filered dataframe"""
        df = df[df['day_of_week'].str.lower() == day]

    return df



def show_raw_data(df):
    
    showdata = input("\nDo you want to see the first 5 rows of the file? If yes, type yes.\n")
    rowstart= 0
    rowend = 5
    maxrows = len(df.index)
    while showdata == 'yes' and rowend < maxrows:
        print(tabulate(df.iloc[rowstart:rowend], headers ="keys"))
        showdata = input("\nDo you want to see the further 5 rows of the file? If yes, type yes.\n")
        rowstart=rowstart + 5
        rowend= rowend + 5
    if (rowend >= maxrows):
        print("Sorry, you reached the end of the file. There are no more rows to display.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """ calculate + display the most common month"""
    month_MostCommon = df['month'].mode()[0]
    print("Most common month for travelling: " + MONTH_DATA[month_MostCommon].title() + " ("+ str(month_MostCommon) + ")")

    """ calculate + display the most common day of week"""
    weekday_MostCommon = df['day_of_week'].mode()[0]
    print("Most common weekday for travelling: " + weekday_MostCommon)


    """ calculate + display the most common start hour"""
    startHour_MostCommon = df['hour'].mode()[0]
    print("Most common hour for travelling: " + str(startHour_MostCommon))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ calculate + display most commonly used start station"""
    startStation_MostCommon = df['Start Station'].mode()[0]
    print("The most common Start Station for travelling: " + startStation_MostCommon)
 
    """ calculate + display most commonly used end station"""
    endStation_MostCommon = df['End Station'].mode()[0]
    print("The most common End Station for travelling: " + endStation_MostCommon)


    """ calculate + display most frequent combination of start station and end station trip"""
    startAndEndStation_MostCommon = ("FROM " + df['Start Station'] + " TO " + df['End Station']).mode()[0]
    print("The most common Start and End Station combination for travelling: " + startAndEndStation_MostCommon)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """calculate + display total travel time"""
    sumOfTravelTime = df['Trip Duration'].sum()
    print("The total travel time is: " + str(sumOfTravelTime))


    """calculate + display mean travel time"""
    MeanTravelTime = df['Trip Duration'].mean()
    print("The mean travel time is: " + str(MeanTravelTime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """calculate + Display counts of user types"""
    countsOfUserTypes = df['User Type'].value_counts()
    print("Count of user types:\n" + str(countsOfUserTypes) + "\n\n")


    """calculate + display birth year and gender --> is not available in washington file"""
    if city == 'chicago' or city == 'new york city':
        # Display counts of gender
        countsOfGender = df['Gender'].value_counts()
        print("Count of user gender:\n")
        print(countsOfGender)
        print("\n\n")
        
        """ Display earliest, most recent, and most common year of birth"""
        """"earliest birth year"""
        earliest_birth_year = int(df['Birth Year'].min())
        print('The earliest birth year of the filtered dataset is: ' + str(earliest_birth_year))

        """Most recent birth year"""
        mostrecent_birth_year = int(df['Birth Year'].max())
        print('The most recent birth year of the filtered dataset is: ' + str(mostrecent_birth_year))
     
        """ Most common birth year"""
        mostcommon_birth_year = int(df['Birth Year'].mode()[0])
        print('The most common birth year of the filtered dataset is: ' + str(mostcommon_birth_year))
    else:
        print("Birth Year and Gender is only available in chicago and new york city. In washington it's not available.")

   


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            show_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except KeyError:
            print("We are sorry, with your selected filters there is no data available. Please start again and pick different filters.\n\n")



if __name__ == "__main__":
	main()
