import requests

BASE_API_URI = "http://telematics.oasa.gr/api/"


class NotFoundLineCodeError(Exception):
    """Raised when no such line code was found"""

    pass


def get_data(parameters):
    response = requests.get(BASE_API_URI, parameters)
    response.raise_for_status()
    return response.json()


def get_linecode_from_lineid(lineid):
    parameters = {"act": "webGetLinesWithMLInfo"}
    data = get_data(parameters)
    for line in data:
        if line["line_id"] == lineid:
            return line["line_code"]
    raise NotFoundLineCodeError


def get_route(linecode):
    parameters = {"act": "webGetRoutes", "p1": linecode}
    data = get_data(parameters)
    for route in data:
        print(f"Code: {route['RouteCode']} Route: {route['RouteDescrEng']}")
    selection = input("Select line (code): ")
    return selection


def get_stop(routecode):
    parameters = {"act": "webGetStops", "p1": routecode}
    data = get_data(parameters)
    for stop in data:
        print(f"Code: {stop['StopCode']} Stop: {stop['StopDescrEng']}")
    selection = input("Select stop (code): ")
    return selection


def get_arrival(stopcode, routecode):
    parameters = {"act": "getStopArrivals", "p1": stopcode}
    data = get_data(parameters)
    # data is null when there are no upcoming buses!
    for route in data:
        if route["route_code"] == routecode:
            print(f"Bus is comming in {route['btime2']} minutes!")


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Get upcoming buses.",
        epilog='Example usage: "%(prog)s --stop 80506"'
        ' or search for stop code: "%(prog)s --line 831"',
    )
    parser.add_argument(
        "--line", type=int, help="line number eg. 831. Returns list of stops"
    )
    parser.add_argument("--route", type=int, help="route number. Returns WHAT")
    parser.add_argument(
        "--stop", nargs="*", type=int, help="stop code(s). Returns upcoming buses"
    )
    parser.add_argument("-V", "--version", action="version", version="2020.05.06")
    args = parser.parse_args()

    lineid = input("Select line (3 digit ID): ")
    linecode = get_linecode_from_lineid(lineid)
    routecode = get_route(linecode)
    stopcode = get_stop(routecode)
    get_arrival(stopcode, routecode)


if __name__ == "__main__":
    main()
