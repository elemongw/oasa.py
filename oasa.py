import urllib.request
import urllib.parse
import json

BASE_API_URI = "http://telematics.oasa.gr/api/"


class LineNotFoundError(Exception):
    pass


class LineCodeNotFoundError(Exception):
    pass


class RouteCodeNotFoundError(Exception):
    pass


def get_data(parameters):
    data = urllib.parse.urlencode(parameters).encode("ascii")
    req = urllib.request.Request(BASE_API_URI, data)
    with urllib.request.urlopen(req) as response:
        parsed = json.loads(response.read().decode())
        return parsed


def get_linecode_from_lineid(lineid):
    parameters = {"act": "webGetLinesWithMLInfo"}
    data = get_data(parameters)
    for line in data:
        if line["line_id"] == str(lineid):
            return line["line_code"]
    raise LineNotFoundError


def get_routes_for_linecode(linecode):
    parameters = {"act": "webGetRoutes", "p1": str(linecode)}
    data = get_data(parameters)
    if not data:
        raise LineCodeNotFoundError
    routes = {}
    for route in data:
        routes[route["RouteCode"]] = route["RouteDescrEng"]
    return routes


def get_stops(routecode):
    parameters = {"act": "webGetStops", "p1": str(routecode)}
    data = get_data(parameters)
    if not data:
        raise RouteCodeNotFoundError
    stops = {}
    for stop in data:
        stops[stop["StopCode"]] = stop["StopDescrEng"]
    return stops


def get_arrival(stopcode, routecode):
    # Valid data is expected in this method
    parameters = {"act": "getStopArrivals", "p1": str(stopcode)}
    data = get_data(parameters)
    # data is null when there are no upcoming buses!
    if not data:
        return None
    for route in data:
        if route["route_code"] == str(routecode):
            return route["btime2"]


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Get upcoming buses.",
        epilog='Example usage: "%(prog)s --stop 80506"'
        ' or search for stop code: "%(prog)s --line 831"',
    )
    parser.add_argument("--line",
                        type=int,
                        help="line number eg. 831. Returns list of stops")
    parser.add_argument("--route",
                        type=int,
                        help="route number. Returns available routes")
    parser.add_argument(
        "--stop",
        nargs="*",
        type=int,
        help=
        "stop code(s). Returns upcoming buses if route is provided as well",
    )
    parser.add_argument("-V",
                        "--version",
                        action="version",
                        version="2020.05.06")
    args = parser.parse_args()

    if args.line:
        return print(get_linecode_from_lineid(args.line))

    if args.route and args.stop:
        return print(get_arrival(args.stop[0], args.route))  # FIXME: order

    if args.route:
        return print(get_routes_for_linecode(args.route))

    if args.stop:
        return print(get_stops(args.stop[0]))

    try:
        lineid = input("Select line (3 digit ID or ctrl-c/ctrl-d to quit): ")
        linecode = get_linecode_from_lineid(lineid)

        routes = get_routes_for_linecode(linecode)
        for route in routes:
            print(f"Code: {route} Route: {routes[route]}")
        routecode = None
        while routecode not in routes:
            routecode = input("Select line (code or ctrl-c/ctrl-d to quit): ")

        stops = get_stops(routecode)
        for stop in stops:
            print(f"Code: {stop} Stop: {stops[stop]}")
        stopcode = None
        while stopcode not in stops:
            stopcode = input("Select stop (code or ctrl-c/ctrl-d to quit): ")

        arrival = get_arrival(stopcode, routecode)
        if arrival:
            print(f"Bus is comming in {arrival} minutes!")
        else:
            print("No upcoming bus found!")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
