import argparse
import json
import time
from datetime import datetime, timedelta


from client import AimHarderClient
# from exceptions import NoBookingGoal


def run_at_specific_time(hour, minute, client: AimHarderClient, target_day: str, class_id1, class_id2):
    """
    Runs the function at a specific time.

    :param hour: hour in 24-hour format (0-23)
    :param minute: minute (0-59)
    """
    target_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time < datetime.now():
        target_time += timedelta(days=1)

    wait_time = (target_time - datetime.now()).total_seconds()
    print(f"Waiting for {wait_time} seconds...")
    time.sleep(wait_time)

    # Call your function here
    print("PreBook",datetime.now().strftime("%H:%M:%S"))
    client.book_class(target_day, class_id1)
    print("After 1st book",datetime.now().strftime("%H:%M:%S"))
    client.book_class(target_day, class_id2)
    print("PostBook",datetime.now().strftime("%H:%M:%S"))


def get_booking_goal_time(day: datetime, booking_goals: json):
    """Get the booking goal that satisfies the given day of the week"""
    try:
        return (
            booking_goals[str(day.weekday())]["time"],
            booking_goals[str(day.weekday())]["name"],
        )
    except KeyError as e:  # did not found a matching booking goal
        raise Exception("Error en booking goals", str(e), booking_goals)


def get_class_to_book(classes: list[dict], target_time: str, class_name: str):
    _classes = list(filter(lambda _class: target_time in _class["timeid"], classes))
    if len(_classes) == 0:
        raise Exception("No hay clases a las "+str(target_time)," Las clases que hay son: ",classes)
    _class = list(filter(lambda _class: class_name in _class["className"], _classes))
    if len(_class) == 0:
        raise Exception("No hay clases de "+str(class_name)+" a las "+str(target_time)," Las clases que hay son: ",_classes)
    return _class[0]["id"]


def main(email="your.email@mail.com", password="1234", box_name="lahuellacrossfit", box_id="3984", days_in_advance="2"):
    print("MAIN: ")
    booking_goals1 = {
        0: {
            "time": "1830_60",
            "name": "Open Box"
        },
        1: {
            "time": "1830_60",
            "name": "Open Box"
        },
        2: {
            "time": "1830_60",
            "name": "Open Box"
        },
        3: {
            "time": "1830_60",
            "name": "Open Box"
        },
        4: {
            "time": "1830_60",
            "name": "Open Box"
        },
        5: {
            "time": "1200_60",
            "name": "Open Box"
        },
        6: {
            "time": "1200_60",
            "name": "Open Box"
        },
    }
    booking_goals2 = {
        0: {
            "time": "1930_60",
            "name": "Open Box"
        },
        1: {
            "time": "1930_60",
            "name": "Open Box"
        },
        2: {
            "time": "1930_60",
            "name": "Open Box"
        },
        3: {
            "time": "1930_60",
            "name": "Open Box"
        },
        4: {
            "time": "1930_60",
            "name": "Open Box"
        },
        5: {
            "time": "1300_60",
            "name": "Open Box"
        },
        6: {
            "time": "1300_60",
            "name": "Open Box"
        },
        
    }
    booking_goals_json1 = json.dumps(booking_goals1)
    booking_goals_json1 = json.loads(booking_goals_json1)
    booking_goals_json2 = json.dumps(booking_goals2)
    booking_goals_json2 = json.loads(booking_goals_json2)
    # print("Booking goals:", booking_goals_json1)
    currentTime_a = datetime.now()
    target_day = datetime.today() + timedelta(days=days_in_advance)
    client = AimHarderClient(
        email=email, password=password, box_id=box_id, box_name=box_name
    )
    target_time1, target_name1 = get_booking_goal_time(target_day, booking_goals_json1)
    target_time2, target_name2 = get_booking_goal_time(target_day, booking_goals_json2)
    classes = client.get_classes(target_day)
    class_id1 = get_class_to_book(classes, target_time1, target_name1)
    class_id2 = get_class_to_book(classes, target_time2, target_name2)
    run_at_specific_time(12, 33, client, target_day, class_id1, class_id2)
    # client.book_class(target_day, class_id1)
    # client.book_class(target_day, class_id2)
    currentTime_b = datetime.now()
    print(
            "Diferencia desde el principio del main:",
            str(int(currentTime_a.strftime("%S")) - int(currentTime_b.strftime("%S"))) + " segundos",
            "\n","Inicio del main: " + str(currentTime_a.strftime("%H:%M:%S")),
            "\n","Fin del main: " + str(currentTime_b.strftime("%H:%M:%S"))
        )


if __name__ == "__main__":
    """
    python src/main.py
     --email your.email@mail.com
     --password 1234
     --box-name lahuellacrossfit
     --box-id 3985
     --booking-goals '{"0":{"time": "1815", "name": "Provenza"}}'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--box-name", required=True, type=str)
    parser.add_argument("--box-id", required=True, type=int)
    # parser.add_argument("--booking-goals", required=False, type=str)
    parser.add_argument("--days-in-advance", required=False, type=int, default=3)

    args = parser.parse_args()
    input = {key: value for key, value in args.__dict__.items() if value != ""}
    main(**input)
