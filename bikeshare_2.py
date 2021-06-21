import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DICT = {  'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6}
DAY_DICT = {'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6}

def get_key(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key
    return 'no such key'


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    valid_cities = ('chicago', 'new york city', 'washington')
    while city.lower() not in valid_cities:
        city = input('Which of the following cities would you like to access data for; Chicago, New York City or Washington? ')
    city = city.lower()
    
    print('Looks like you\'ve chosen ' +city +'. If this is incorrect, restart the program now.')

    month = ''
    day = '' 

    # get user input for which filters to apply
    filter = ''
    valid_filters = ('month', 'day', 'both', 'neither')
    while filter.lower() not in valid_filters:
        filter = input('Would you like to filter ' +city +' data by month, day, both or neither?')
    
    if filter.lower() == 'month':
        day = 'all'
    elif filter.lower() == 'day':
        month = 'all'
    elif filter.lower() == 'neither':
        day, month = 'all','all'

    # get user input for month (all, january, february, ... , june)
    valid_months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while month.lower() not in valid_months:
        month = input('Which month would you like to see ' +city +' data for? January, February, March, April, May, June')
    month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    while day.lower() not in valid_days:
        day = input('Which day of the week would you like to see data for? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
    day = day.lower()

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
    # reads the selected city csv and adds two columns to the dataframe with our potential filters
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['Starting Hour'] = df['Start Time'].dt.hour
    
    # filters our dataframe based on the input from the user
    if month in MONTH_DICT.keys():
        month = MONTH_DICT[month]  
    if day in DAY_DICT.keys():
        day = DAY_DICT[day]
    
    if month == 'all':
        if day == 'all':
             return df
        else: 
            df = df[df['Day']==day]
    elif day == 'all':
        df = df[df['Month']==month]
    else: 
        df = df[(df['Month']==month) & (df['Day']==day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    count_month = (df['Month'] == common_month).sum()
    month_long = get_key(common_month, MONTH_DICT)
    print('The most common month is ' + month_long)
    print('It occurs '+str(count_month) +' times')

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    count_day = (df['Day'] == common_day).sum()
    day_long = get_key(common_day, DAY_DICT)
    print('The most common day of week is ' + day_long)
    print('It occurs '+str(count_day) +' times')

    # display the most common start hour
    common_start_hour = df['Starting Hour'].mode()[0]
    count_start_hour = (df['Starting Hour'] == common_start_hour).sum()
    print('The most common starting hour is ' + str(common_start_hour))
    print('It occurs '+str(count_start_hour) +' times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    count_start = (df['Start Station'] == most_common_start).sum()
    print('The most commonly used starting station is '+most_common_start)
    print('It occurs '+str(count_start) +' times')

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    count_end = (df['End Station'] == most_common_end).sum()
    print('The most commonly used end station is '+most_common_end)
    print('It occurs '+str(count_end) +' times')

    # display most frequent combination of start station and end station trip
    most_common_combo = (df['Start Station'] +' ' + df['End Station']).mode()[0]
    count_combo = (df['Start Station'] +' ' + df['End Station'] == most_common_combo).sum()
    print('The most common combination of start- and end station is '+most_common_combo)
    print('It occurs '+str(count_combo) +' times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is ' +str(total_travel_time) +' seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is ' +str(mean_travel_time) +' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print('This data has no gender details for the user base')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()
        print('The earliest birth year is '+ str(earliest_birth_year))
        print('The most recent birth year is '+ str(most_recent_birth_year))
        print('The most common birth year is '+ str(most_common_birth_year))
    else:
        print('This data has no birth year details for the user base')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """Displays the raw data 5 lines at a time"""
    display_data = input('Would you like to see the first 5 lines of the raw data? Enter yes or no').lower()
    if display_data == 'yes':
        start_loc = 0
        answer = True
        while (answer):
            print(df.iloc[start_loc: start_loc + 5]) 
            start_loc +=5
            prompt = input('Would you like to continue? Enter yes or no ').lower()
            if prompt == 'no':
                answer = False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
