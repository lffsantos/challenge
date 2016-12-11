import os
import pytest

from prog3.invite_customers import degrees_to_radians, InviteCustomers


@pytest.mark.parametrize('coordinate_degree, coordinate_rad', [
    ((53.3393, -6.2576841), (0.93094640571, -0.10921719109)),
    ((53.1229599, -9.436036), (0.92717055866, -0.16468989654)),
    ((51.802, -8), (0.90411545912, -0.13962634016)),
    ((53, -5.920898), (0.92502450356, -0.10333916477)),
    (("53.3393", -6.2576841), TypeError),
])
def test_degrees_to_radians(coordinate_degree, coordinate_rad):
    if coordinate_rad == TypeError:
        with pytest.raises(TypeError):
            degrees_to_radians(coordinate_degree)
    else:
        lat, long = degrees_to_radians(coordinate_degree)
        assert (round(lat, 11), round(long, 11)) == coordinate_rad


class TestInviteCustomers():

    def setup(self):
        self.invite = InviteCustomers((53.3393, -6.2576841))

    @pytest.mark.parametrize('office_location, limit_distance, exception_error', [
        ((53.3393, -6.2576841), None, TypeError),
        ((53.3393, -4), 80, None),
        (('10.00', -22.0909), None, TypeError),
        ((10.00, '10.00'), None, TypeError),
        ((53.3393, -22.0909), '100', TypeError),
        ([53.3393, -22.0909], 22, TypeError),
    ])
    def test_init(self, office_location, limit_distance, exception_error):
        if exception_error == TypeError:
            with pytest.raises(TypeError):
                InviteCustomers(office_location, limit_distance)
        else:
            InviteCustomers(office_location, limit_distance)
        pass

    @pytest.mark.parametrize('file_name, expected_customers', [
        ('customers_test.json', {
            4: 'Ian Kehoe',
            5: 'Nora Dempsey',
            12: 'Christina McArdle',
        }),
        ("customers_test1.json", FileNotFoundError),
        (None, ValueError),
        ("customers_invalid_test.json", KeyError)
    ])
    def test_load_customers(self, file_name, expected_customers):
        path_file_name = file_name if not file_name else os.path.abspath(
            os.path.join(os.path.dirname(__file__), file_name)
        )
        if expected_customers in [FileNotFoundError, KeyError, ValueError]:
            with pytest.raises(expected_customers):
                self.invite.load_customers(file_name=path_file_name)
        else:
            customers_near_the_office = self.invite.load_customers(file_name=path_file_name)
            assert customers_near_the_office == expected_customers

    @pytest.mark.parametrize('customer_location, distance_expected', [
        ((52.986375, -6.043701), 41.755813545096565),
        ((51.92893, -10.27699), 313.24768450696104),
        ((51.8856167, -10.4240951), 324.3670068155382),
        ((52.3191841, -8.5072391), 188.949920038136),
        ((53.807778, -7.714444), 109.38219327418832),
        ((53.4692815, -9.436036), 211.1720126163795),
        ((54.0894797, -6.18671), 83.5468161909727),
        ((53.038056, -7.653889), 98.86864753879988)
    ])
    def test_distance_between_office_customer(self, customer_location, distance_expected):
        distance = self.invite.distance_between_office_customer(customer_location)
        assert distance == distance_expected

    @pytest.mark.parametrize('distance, expected', [
        (100, True), (900, False), (89.90, True), (99.99, True), (100.05, False)
    ])
    def test_is_near_the_office(self, distance, expected):
        assert self.invite.is_near_the_office(distance) == expected

    @pytest.mark.parametrize('customer_list, save_in_file, file_path_name', [
        ({
            4: 'Ian Kehoe',
            5: 'Nora Dempsey',
            12: 'Christina McArdle',
        }, False, None),
        ({
            4: 'Ian Kehoe',
            5: 'Nora Dempsey',
            12: 'Christina McArdle',
        }, True, 'guest_test.txt'),
    ])
    def test_guest_list(self, customer_list, save_in_file, file_path_name):
        path_file_name = None if not file_path_name else os.path.abspath(
            os.path.join(os.path.dirname(__file__), file_path_name)
        )
        self.invite.guest_list(customer_list, save_in_file, path_file_name)
        if save_in_file:
            assert os.path.isfile(path_file_name)
            self.invite.guest_list(customer_list, save_in_file, path_file_name)
            os.remove(path_file_name)
            assert not os.path.isfile(path_file_name)
