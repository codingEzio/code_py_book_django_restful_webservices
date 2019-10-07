from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.contrib.auth.models import User

from rest_framework import status as rest_status_code
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from drones import views
from drones.models import DroneCategory, Pilot


class DroneCategoryTests(APITestCase):
    """ Two of our helpers were to add data to the database,
    and it was used by every other methods to create the initial data.
    Q: Why?  (quote: https://stackoverflow.com/a/3885518/6273859)
    A: "if it is a unit test, it should be able to run on its own".
    """

    VERSION_PREFIX = '/v1'
    PRINT_MSG_PREFIX = '[PRINT] '

    def helper_post_drone_category(self, name):
        url = reverse(views.DroneCategoryList.name)
        data = { 'name': name }
        response = self.client.post(url, data, format='json')

        return response

    def helper_post_drone_category_plus_url(self, name):
        url = self.VERSION_PREFIX + reverse(views.DroneCategoryList.name)
        data = { 'name': name }
        response = self.client.post(url, data, format='json')

        return response, url

    def test_post_and_get_drone_category(self):
        new_drone_category_name = 'Hexacopter'
        response, url = self.helper_post_drone_category_plus_url(new_drone_category_name)

        # You can only see this if you add the '--capture=no' flag
        # of course you should avoid using 'print' statements in tests!
        print(f"{self.PRINT_MSG_PREFIX}pk  : {DroneCategory.objects.get().pk}")
        print(f"{self.PRINT_MSG_PREFIX}url : {url}")

        assert response.status_code == rest_status_code.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category_name(self):
        url = reverse(views.DroneCategoryList.name)
        new_drone_category_name = 'Duplicated Copter'
        data = { 'name': new_drone_category_name }

        response_one = self.helper_post_drone_category(new_drone_category_name)
        assert response_one.status_code == rest_status_code.HTTP_201_CREATED

        response_two = self.helper_post_drone_category(new_drone_category_name)
        assert response_two.status_code == rest_status_code.HTTP_400_BAD_REQUEST

    def test_get_drone_category(self):
        drone_category_name = 'Easy to retrieve'
        response = self.helper_post_drone_category(drone_category_name)
        url = self.VERSION_PREFIX + reverse(views.DroneCategoryDetail.name,
                                            None,
                                            { response.data['pk'] })
        get_response = self.client.get(url, format='json')

        assert get_response.status_code == rest_status_code.HTTP_200_OK
        assert get_response.data['name'] == drone_category_name

    def test_get_drone_categories_collection(self):
        new_drone_category_name = 'Super Capter'
        self.helper_post_drone_category(new_drone_category_name)
        url = self.VERSION_PREFIX + reverse(views.DroneCategoryList.name)
        response = self.client.get(url, format='json')

        assert response.status_code == rest_status_code.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_drone_category_name

    def test_filter_drone_category_by_name(self):
        drone_category_name_one = 'Hexacopter'
        drone_category_name_two = 'Octocopter'
        self.helper_post_drone_category(drone_category_name_one)
        self.helper_post_drone_category(drone_category_name_two)

        filter_by_name = { 'name': drone_category_name_one }
        url = (f'{self.VERSION_PREFIX + reverse(views.DroneCategoryList.name)}'
               f'?{urlencode(filter_by_name)}')
        response = self.client.get(url, format='json')

        print(f"{self.PRINT_MSG_PREFIX}url      : {url}")
        print(f"{self.PRINT_MSG_PREFIX}response : {response}")

        assert response.status_code == rest_status_code.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == drone_category_name_one

    def test_update_drone_category(self):
        drone_category_name = 'Category Initial Name'
        response = self.helper_post_drone_category(drone_category_name)
        url = self.VERSION_PREFIX + reverse(views.DroneCategoryDetail.name,
                                            None,
                                            { response.data['pk'] })

        updated_drone_category_name = 'Updated Name'
        data = { 'name': updated_drone_category_name }
        patch_response = self.client.patch(url, data, format='json')

        assert patch_response.status_code == rest_status_code.HTTP_200_OK
        assert patch_response.data['name'] == updated_drone_category_name


class PilotTests(APITestCase):
    VERSION_PREFIX = '/v1'
    PRINT_MSG_PREFIX = '[PRINT] '

    def helper_post_pilot(self, name, gender, races_count):
        url = self.VERSION_PREFIX + reverse(views.PilotList.name)
        data = { 'name'       : name,
                 'gender'     : gender,
                 'races_count': races_count, }
        response = self.client.post(url, data, format='json')

        print(f'{self.PRINT_MSG_PREFIX}url : {url}')
        return response

    def helper_create_user_and_set_token_credentials(self):
        user = User.objects.create_user('user01',
                                        'user01@haha.com',
                                        'user01password')
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_post_and_get_pilot(self):
        self.helper_create_user_and_set_token_credentials()
        new_pilot_name = 'Nancy'
        new_pilot_gender = Pilot.FEMALE
        new_pilot_races_count = 3

        response = self.helper_post_pilot(new_pilot_name,
                                          new_pilot_gender,
                                          new_pilot_races_count)
        print(f'{self.PRINT_MSG_PREFIX}nPk : {Pilot.objects.get().pk}')

        assert response.status_code == rest_status_code.HTTP_201_CREATED
        assert Pilot.objects.count() == 1
        saved_pilot = Pilot.objects.get()

        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.races_count == new_pilot_races_count

        url = self.VERSION_PREFIX + reverse(views.PilotDetail.name,
                                            None,
                                            { saved_pilot.pk })
        authorized_get_response = self.client.get(url, format='json')
        assert authorized_get_response.status_code == rest_status_code.HTTP_200_OK
        assert authorized_get_response.data['name'] == new_pilot_name

        self.client.credentials()
        unauthorized_get_response = self.client.get(url, format='json')
        assert unauthorized_get_response.status_code == rest_status_code.HTTP_401_UNAUTHORIZED

    def test_try_to_post_pilot_without_token(self):
        new_pilot_name = 'Unauthorized Pilot'
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 2
        response = self.helper_post_pilot(new_pilot_name,
                                          new_pilot_gender,
                                          new_pilot_races_count)

        print(f'{self.PRINT_MSG_PREFIX}response    : {response}')
        print(f'{self.PRINT_MSG_PREFIX}pilot count : {Pilot.objects.count()}')

        assert response.status_code == rest_status_code.HTTP_401_UNAUTHORIZED
        assert Pilot.objects.count() == 0
