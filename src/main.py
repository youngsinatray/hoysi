import argparse
import json
from datetime import datetime, timedelta


from client import AimHarderClient
from exceptions import NoBookingGoal


def get_booking_goal_time(day: datetime, booking_goals: json):
    """Get the booking goal that satisfies the given day of the week"""
    try:
        print(str(day.weekday()))
        return (
            booking_goals[str(day.weekday())]["time"],
            booking_goals["0"]["name"],
        )
    except KeyError as e:  # did not found a matching booking goal
        raise Exception("Error en booking goals", str(e), booking_goals)


def get_class_to_book(classes: list[dict], target_time: str, class_name: str):
    classes = list(filter(lambda _class: target_time in _class["timeid"], classes))
    _class = list(filter(lambda _class: class_name in _class["className"], classes))
    if len(_class) == 0:
        raise NoBookingGoal
    return _class[0]["id"]


def main(email="your.email@mail.com", password="1234", box_name="lahuellacrossfit", box_id="3984", days_in_advance="2", booking_goals='{"0":{"time": "1815", "name": "Provenza"}}'):
    print("MAIN: ")
    booking_goals = {
        0: {
            "time": "1830_60",
            "name": "Open Box"
        },
        0: {
            "time": "1930_60",
            "name": "Open Box"
        },
        1: {
            "time": "1830_60",
            "name": "Open Box"
        },
        1: {
            "time": "1930_60",
            "name": "Open Box"
        },
        2: {
            "time": "1830_60",
            "name": "Open Box"
        },
        2: {
            "time": "1930_60",
            "name": "Open Box"
        },
        3: {
            "time": "1830_60",
            "name": "Open Box"
        },
        3: {
            "time": "1930_60",
            "name": "Open Box"
        },
        4: {
            "time": "1830_60",
            "name": "Open Box"
        },
        4: {
            "time": "1930_60",
            "name": "Open Box"
        },
        5: {
            "time": "1230_60",
            "name": "Open Box"
        },
        5: {
            "time": "1330_60",
            "name": "Open Box"
        },
        6: {
            "time": "1230_60",
            "name": "Open Box"
        },
        6: {
            "time": "1330_60",
            "name": "Open Box"
        },
        
    }
    booking_goals_json = json.dumps(booking_goals)
    booking_goals_json = json.loads(booking_goals_json)
    print("Booking goals:", booking_goals_json)
    currentTime_a = datetime.now().strftime("%S")
    target_day = datetime.today() + timedelta(days=days_in_advance)
    client = AimHarderClient(
        email=email, password=password, box_id=box_id, box_name=box_name
    )
    target_time, target_name = get_booking_goal_time(target_day, booking_goals_json)
    classes = client.get_classes(target_day)
    class_id = get_class_to_book(classes, target_time, target_name)
    client.book_class(target_day, class_id)
    currentTime_b = datetime.now().strftime("%S")
    print("Diferencia:", str(int(currentTime_a) - int(currentTime_b)) + " segundos")


if __name__ == "__main__":
    """
    python src/main.py
     --email your.email@mail.com
     --password 1234
     --box-name lahuellacrossfit
     --box-id 3984
     --booking-goal '{"0":{"time": "1815", "name": "Provenza"}}'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--box-name", required=True, type=str)
    parser.add_argument("--box-id", required=True, type=int)
    parser.add_argument("--booking-goals", required=True, type=str)
    parser.add_argument("--days-in-advance", required=False, type=int, default=3)

    args = parser.parse_args()
    input = {key: value for key, value in args.__dict__.items() if value != ""}
    main(**input)
