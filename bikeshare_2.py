import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid Inputs. Try again!')

    # get user input for filter by month, day or not
    while True:
        filter_by = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. ').lower()
        if filter_by in ['month', 'day', 'both', 'none']:
            break
        else:
            print('Invalid Inputs. Try again!')

    # get user input for month (all, january, february, ... , june)
    if filter_by in ['month', 'both']:
        while True:
            month = input('Which month - January, February, March, April, May, or June? ').lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Invalid Inputs. Try again!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_by in ['day', 'both']:
        while True:
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('Invalid Inputs. Try again!')
    
    # give 'all' for no filter
    if filter_by == 'none':
        month, day = 'all', 'all'
    elif filter_by == 'month':
        day = 'all'
    elif filter_by == 'day':
        month = 'all'

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[(df['month'] == month)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[(df['day_of_week'] == day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]
    print('Most popular month for traveling: {}'.format(pop_month))

    # display the most common day of week
    pop_dow = df['day_of_week'].mode()[0]
    print('Most popular day of week for traveling: {}'.format(pop_dow))

    # display the most common start hour
    pop_hour = df['Start Time'].dt.strftime("%H").mode()[0]
    print('Most popular hour for traveling: {}'.format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('Most popular Start Station: {}'.format(pop_start_station))

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('Most popular End Station: {}'.format(pop_end_station))

    # display most frequent combination of start station and end station trip
    pop_combi_station = (df['Start Station'] + ' --> ' + df['End Station']).mode()[0]
    print('Most popular trip: {}'.format(pop_combi_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Duration:', df['Trip Duration'].sum())

    # display mean travel time
    print('Avg Duration:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cnt_user_type = df['User Type'].value_counts()
    print('Subscribers: {}, Customers: {}'.format(cnt_user_type['Subscriber'], cnt_user_type['Customer']))
    
    try:
        # Display counts of gender
        cnt_user_gender = df['Gender'].value_counts()
        print('Male: {}, Female: {}'.format(cnt_user_gender['Male'], cnt_user_gender['Female']))

        # Display earliest, most recent, and most common year of birth
        earlist_user_birth = df['Birth Year'].min()
        latest_user_birth = df['Birth Year'].max()
        common_user_birth = df['Birth Year'].mode()[0]
        print('Earliest year of birth: {}\nMost Recent year of birth: {}\nMost Common year of birth: {}\n'.format(earlist_user_birth, latest_user_birth, common_user_birth))
    except:
        print('No Info about Gender and Birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Display raw data if the user wants"""
    for i in range(0, len(df), 5):
        show_raw_data = input('Would you like to view (5 more) individual trip data? (Type "no" if you don\'t want): ')
        if show_raw_data.lower() == 'no':
            break
        print(df[i:i+5])

def main():
    while True:
        city, month, day = get_filters()
        print('We will show you data about {} filtered by\nMonth: {}, Day: {}'.format(city.title(), month.title(), day.title()))
        print("Just one moment... loading the data")
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
