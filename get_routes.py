import requests
import json
import datetime
TIMEZONE_DIFF = 4

def parse_step(steps_dict, route_data):
    directions_string = ""
    first_bus_depart_time = ""
    first_bus_num= ""
    first_bus_found = False
    for step in steps_dict:
        if step['travel_mode'] == "WALKING":
            directions_string += "\U0001F6B6 > "
        if step['travel_mode'] == "TRANSIT":
            transit_num = step['transit_details']['line']['short_name']
            directions_string += "\U0001F68C {} > ".format(transit_num)

            if not first_bus_found:
                depart_time = step['transit_details']['departure_time']['text']
                first_bus_depart_time = depart_time
                first_bus_num = transit_num
                first_bus_found = True
    directions_string = directions_string[:len(directions_string) - 3]  # cut string
    route_data.append(directions_string)
    route_data.append(first_bus_depart_time)
    route_data.append(first_bus_num)

def call_google_api(epoch):
    destination = "<YOUR_ADDRESS_DESTINATION>"
    origin = "<YOUR_ADDRESS_ORIGIN>"
    key = "<YOUR_API_KEY>"

    arrival_time = epoch
    mode = "transit"

    url = "https://maps.googleapis.com/maps/api/directions/json?destination={}&origin={}&mode={}&key={}&arrival_time={}&alternatives=true".format(destination, origin, mode, key, arrival_time)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    routes_dict = response.json()

    # ###### DEBUG ######
    # with open("routes.json", "w") as outfile:
    #     json.dump(response.json(), outfile)
    # routes_dict = get_json_from_file('routes.json')
    # ###### DEBUG ######
    
    if 'routes' not in routes_dict:
        # there is some error
        return
    routes_list_to_return = []
    routes_dict = routes_dict['routes']
    for route in routes_dict:
        route_data = []
        parse_step(route['legs'][0]['steps'], route_data)
        route_data.append(route['legs'][0]['arrival_time']['text'])
        routes_list_to_return.append(route_data)

    return routes_list_to_return

# get dict from json file
def get_dict_from_json_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def convert_day_str_to_int(s):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return days.index(s.lower())

def find_num_days_between(today_day, course_day):
    if course_day > today_day:
        return course_day - today_day
    elif course_day < today_day:
        return 7 - (today_day - course_day)
    return 0

def parse_hr(s):
    s = s.lower()
    if 'pm' in s and '12' in s:
        return 12
    elif 'am' in s and '12' not in s:
        return int(s[:s.find(":")])
    elif 'pm' in s:
        return int(s[:s.find(":")]) + 12
    return 0

def parse_min(s):
    s=s.lower()
    return int(s[s.find(":")+1:s.find("m")-1])

def calculate_next_class():
    today_dt = datetime.datetime.today()
    today_epoch = today_dt.strftime('%s')
    today_day = today_dt.weekday()

    courses = get_dict_from_json_file('schedule.json')['courses']

    schedule_epoch_list = []
    for course in courses:
        course_dt = today_dt + datetime.timedelta(days=find_num_days_between(today_day=today_day, course_day=convert_day_str_to_int(course['course_day'])))
        course_st = course['course_starting_time']
        # add timezone_diff to offset the hours since the timezone for schedule.json is in EDT time
        course_dt = course_dt.replace(hour=parse_hr(course_st), minute=parse_min(course_st), second=0) + datetime.timedelta(hours=TIMEZONE_DIFF)
        course_epoch = course_dt.strftime('%s')

        # only appends to list if course is after current time
        if int(course_epoch) > int(today_epoch):
            schedule_epoch_list.append([course_epoch, course['course_name'], course_st, course['course_day']])

    return min(schedule_epoch_list, key=lambda x:x[0])

def get_today_date():
    today_dt = datetime.datetime.today() - datetime.timedelta(hours=TIMEZONE_DIFF)    
    return today_dt.strftime('%c')

def calculate_epoch(year, month, day, hours, minutes=0, seconds=0):
    # year/month/day/hours/minutes/seconds:milliseconds
    epoch = datetime.datetime(year, month, day, hours, minutes, seconds).strftime('%s')
    return epoch