import argparse
import collections
import json
import logging
import os

from math import radians, cos, sin, acos


logging.basicConfig(level=logging.INFO, format='%(message)s')


def degrees_to_radians(coordinate):
    """
    Convert degrees to radians. if coordinate is not valid raise exception
    :param coordinate: tuple (latitude, longitude) in degrees
    :return: (latitude, longitude)
    """
    if is_valid_coordinate(coordinate):
        lat, long = map(radians, list(coordinate))

    return lat, long


def is_valid_coordinate(coordinate):
    if not isinstance(coordinate, tuple):
        raise TypeError('coordinate expected a tuple but received {}'.format(
            type(coordinate).__name__
        ))
    if len(coordinate) != 2 or (
                not isinstance(coordinate[0], (int, float)) or not isinstance(
                    coordinate[1], (int, float))):
        raise TypeError(
            'coordinate expected a tuple (int/float, int/float) '
            'but received ({}, {})'.format(
                type(coordinate[0]).__name__, type(coordinate[1]).__name__
            )
        )
    return True


class InviteCustomers():
    global R
    R = 6371  # R is earth’s radius (mean radius = 6,371km);

    def __init__(self, office_location, limit_distance=100):
        if is_valid_coordinate(office_location):
            self.office_latitude, self.office_longitude = degrees_to_radians(office_location)
        if not isinstance(limit_distance, (int, float)):
            raise TypeError(
                'limit_distance expected int or float but received {}'.format(
                    type(limit_distance).__name__
                ))
        self.limit_distance = limit_distance

    def load_customers(self, file_name='customers.json'):
        customers_near_the_office = {}
        if not os.path.isfile(file_name):
            raise FileNotFoundError('No such file or directory: {}'.format(file_name))

        with open(file_name) as data_file:
            for line in data_file:
                line = json.loads(line)
                try:
                    distance = self.distance_between_office_customer(
                        (float(line['latitude']), float(line['longitude']))
                    )
                    if self.is_near_the_office(distance):
                        customers_near_the_office[line['user_id']] = line['name']
                except KeyError as error:
                    raise KeyError('invalid file key : "{}" not found'.format(
                        error.args[0])
                    )

        return customers_near_the_office

    def distance_between_office_customer(self, customer_location):
        """
        Receive the customer location in degrees and calculate the distance to the office.
        :param customer_location: tuple (latitude, longitude) in degrees
        :return: distance in km.
        """
        lat_customer, long_customer = degrees_to_radians(customer_location)
        delta_x = acos(
            sin(self.office_latitude) * sin(lat_customer) +
            cos(self.office_latitude) * cos(lat_customer) *
            cos(self.office_longitude - long_customer)
        )
        return delta_x * R

    def is_near_the_office(self, distance):
        return True if round(distance, 2) <= self.limit_distance else False

    @staticmethod
    def guest_list(customers_near, save_in_file=False, guest_list_file='guest_list.txt'):
        """
        Receive a dictionary of customer to send invite puts in order by id and print
        the values at screen. If save_in_fale=True, save an file with customer
        to send invite.
        :param customers_near: dictionary {'id': 'name'}
        :param save_in_file: optional
        :param guest_list_file:
        :return:
        """
        guests = collections.OrderedDict(sorted(customers_near.items()))
        if save_in_file:
            if os.path.isfile(guest_list_file):
                logging.warning(
                    'Removing existing file "{}" and create new'.format(guest_list_file)
                )
                os.remove(guest_list_file)

            with open(guest_list_file, 'a') as data_file:
                for user_id, name in guests.items():
                    logging.info(str(user_id) + ' - ' + name)
                    data_file.write(str(user_id) + ' - ' + name + ' \n')
        else:
            for user_id, name in guests.items():
                print(str(user_id) + ' - ' + name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Invite Customers')

    parser.add_argument('-c', '--coordinate', nargs=2, type=float,
                        action='append', help='Office Coordinate (Latitude, Longitude) '
                                              'in degrees e.g : 53.3393, -6.2576841')
    parser.add_argument('--customers-path-name',
                        help='path_name the file of customer')
    parser.add_argument('-s', '--save', default=False,
                        help='save guest list in file')
    parser.add_argument('-g', '--guest-path-name', default='guest_list.txt',
                        help='location for save customers for invite')

    args = parser.parse_args()
    local_file_customers = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'customers.json')
    )
    if args.customers_path_name:
        local_file_customers = args.customers_path_name

    save_in_file = False
    if args.save == 'true' or args.save == 'True':
        save_in_file = True

    office_coordinate = (53.3393, -6.2576841)
    if not args.coordinate:
        logging.info("Use Dublin office coordinate : (53.3393, -6.2576841)")
        office_coordinate = (53.3393, -6.2576841)
    else:
        office_coordinate = tuple(args.coordinate[0])

    invite = InviteCustomers(office_coordinate)
    invite.guest_list(
        invite.load_customers(local_file_customers), save_in_file=save_in_file,
        guest_list_file=args.guest_path_name
    )
