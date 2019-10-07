from django.core.urlresolvers import reverse

from rest_framework import status as rest_status_code
from rest_framework.test import APITestCase

from drones import views
from drones.models import DroneCategory


class DroneCategoryTests(APITestCase):
    version_prefix = '/v1'

    def helper_post_drone_category(self, name):
        url = reverse(views.DroneCategoryList.name)
        data = { 'name': name }
        response = self.client.post(url, data, format='json')

        return response

    def helper_post_drone_category_plus_url(self, name):
        url = self.version_prefix + reverse(views.DroneCategoryList.name)
        data = { 'name': name }
        response = self.client.post(url, data, format='json')

        return response, url

    def test_post_and_get_drone_category(self):
        new_drone_category_name = 'Hexacopter'
        response, url = self.helper_post_drone_category_plus_url(new_drone_category_name)

        # You can only see this if you add the '--capture=no' flag
        # of course you should avoid using 'print' statements in tests!
        print(f"[PRINT] pk  : {DroneCategory.objects.get().pk}")
        print(f"[PRINT] url : {url}")

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
