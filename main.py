from bus_route import BusRoute
from ui import run


def main():
    """Create the route with sample stops and launch the interface. O(1)."""
    route = BusRoute()
    route.add_first("Terminal")
    route.add_last("Plaza")
    route.add_last("Hospital")
    route.add_last("Universidad")
    run(route)


if __name__ == "__main__":
    main()
