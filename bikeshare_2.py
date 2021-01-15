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
    print('Hello! Let\'s explore some US bikeshare data!')
    print('The program will ask you for a (1) city, (2) a month, and a (3) day of the week.\n')

    # get user input for one of three city names.
    city = ''
    while city not in CITY_DATA.keys():
        city = input('Please choose the city: Chicago, New York City, Washington:\n').lower()
        if city not in CITY_DATA.keys():
            print('Your input does not match to available options!\n')
    print('You have choosen {}.\n'.format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month = ''
    available_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in available_months:
        month = input('Investigate all or selected months. Choose from: All, January, February, March, April, May, '
                      'June:\n').lower()
        if month not in available_months:
            print('Your input does not match the available options!')
            print('If no month should be selected, type \"all\".\n')
    print('You have choosen {}.\n'.format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    available_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in available_days:
        day = input('Investigate all or selected days. Choose from All, Monday, Tuesday, Wednesday, Thursday, '
                    'Friday, Saturday, Sunday:\n').lower()
        if day not in available_days:
            print('Your input does not match the available options!')
            print('If no particular day of the week should be selected, type \"all\".\n')
    print('You have chosen {}.\n'.format(day.title()))

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
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['hour'] = df['Start Time'].dt.hour

    # make new column for trip information
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('-' * 40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        # use list for getting name of month. alternatively use calendar
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        most_common_month = months[most_common_month - 1]
        print('The most common month is {}.'.format(most_common_month))
    else:
        print('You have chosen {} for analysis. No statistics on most frequent months.'.format(month.title()))

    # display the most common day of week

    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        print('The most common day of the week is {}.'.format(most_common_day))
    else:
        print('You have chosen {} for analysis. No statistics on most frequent days of the week.'.format(day.title()))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is {}.'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('-' * 40)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # common_start_station = df['Start Station'].mode()[0] did not work on my Python version
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_trip = df['Trip'].mode()[0]
    print('The most common trip is {}.'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    global mean_time
    print('-' * 40)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # divmod seems to be the most clean and readable way, taken from geeksforgeeks.org
    total_time = df['Trip Duration'].sum()
    print('Total travel time:', total_time)
    total_min, total_sec = divmod(total_time, 60)
    total_hour, total_min = divmod(total_min, 60)
    print('The total travel time is {} hour(s), {} minute(s) and {} second(s).\n'.format(total_hour, int(total_min),
                                                                                         round(total_sec, 1)))

    # display mean travel time
    # numbers have to be cut off after decimal point
    mean_time = df['Trip Duration'].mean()
    mean_min, mean_sec = divmod(mean_time, 60)
    print('The mean trip duration is {} minute(s) and {} second(s).\n'.format(int(mean_min), round(mean_sec, 1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # I use to_frame to improve readability. Taken from re-thought.com/pandas-value_counts
    user_type_count = df['User Type'].value_counts()
    print('User types and their counts: \n{}'.format(user_type_count.to_frame('Frequency')))
    print()

    # Display counts of gender
    # As Washington has no gender information, there is a if included, alternatively use try,except
    if 'Gender' not in df.columns:
        print('There is no gender information for this city.')
    else:
        gender_count = df['Gender'].value_counts()
        print('Genders and their counts: \n{}'.format(gender_count.to_frame('Frequency')))
    print()

    # Display earliest, most recent, and most common year of birth
    # As not all data sets have this information, I include an if:
    if 'Birth Year' not in df.columns:
        print('There is no more detailed user information for this city.')
    else:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('More detailed information on users year of birth:')
        print(
            'Oldest user is born in {} and youngest user is born in {}.'.format(int(earliest_birth), int(recent_birth)))
        print('The average year of birth is {}.'.format(int(common_birth)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    # request from reviewer. This part has been added in the second version
    # As there are two variables (view_data and view_display), I start with if and use inside a while loop

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0

    if view_data == 'yes':
        # The pd.set_option is from towardsdatascience.com/how-to-show-all-columns-rows-of-a-pandas-dataframe-c49d4507fcf
        pd.set_option('display.max_columns', None)
        print('\nPrint of raw data:\n')
        while True:
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_display = input('\nDo you wish to continue?\n').lower()

            if view_display == 'no':
                break

    else:
        print('No raw data displayed.')

    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
