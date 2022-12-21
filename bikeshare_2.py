import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the name of City ( Chicago , New York City , Washington ) :  ").lower()

    while city not in cities:
        city = input("You Enter Wrong City ! , Enter the name of City :  ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter the name of Month (1st 6 Month)  :  ").lower()
    while month not in months:
        month = input("You Enter Wrong Month ! , Enter the name of Month :  ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the name of Day  :  ").lower()
    while day not in days:
        day = input("You Enter Wrong Day ! , Enter the name of Day :  ").lower()

    print('-' * 40)
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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month :', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular day :', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Combination'] = df["Start Station"] + " -- " + df["End Station"]
    combination = df['Combination'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station:  ', combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print("The Total Travel Time in Hours  is %s Hours :  " % time.strftime("%H:%M:%S", time.gmtime(travel_time)))

    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print("The  Travel Time Mean in Hours is  %s  Hours :  " % time.strftime("%H:%M:%S", time.gmtime(travel_time_mean)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    except KeyError:
        print('No Gender in this City File')

    # Display earliest, most recent, and most common year of birth

    try:
        earliest = df['Birth Year'].min()
        print('Earliest Birth Year is :  \n', earliest)

        most_recent = df['Birth Year'].max()
        print('Most Recent Birth Year is :  \n', most_recent)

        popular_birth_day = df['Birth Year'].mode()[0]
        print('Most Popular Birth Year:  \n', popular_birth_day)

    except KeyError:
        print('No Birth Year in this City File')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    data = input('\nWould you Want to See Raw data? Enter yes or no.\n').lower()
    while data == 'yes':
        df.sample(n=5)
        print(df.sample(n=5))
        data = input('\nWould you Want to See Raw data? Enter yes or no.\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
