from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from toys.models import Toy
from toys.serializers import ToySerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def toy_list(request):
    if request.method == 'GET':
        # $ http :8000/toys/
        # $ curl -iX GET localhost:8000/toys/
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return JSONResponse(toys_serializer.data)

    elif request.method == 'POST':
        # $ http POST :8000/toys/ name="Sokoban" \
        #   description="a mobile game" \
        #   toy_category="Electronics" \
        #   was_included_in_home=false \
        #   release_date="2017-03-12T01:01:00.656665Z"
        #
        # $ curl -iX POST -H "Content-Type: application/json" -d
        #   '{"name":"Tomb raider","description":"a mobile game",
        #   "toy_category":"Electronics","was_included_in_home":"false",
        #   "release_date":"2016-05-25T01:01:00.652465Z"}' localhost:8000/toys/
        toy_data = JSONParser().parse(request)  # parsed to native types

        toy_serializer = ToySerializer(data=toy_data)  # "rendered" by our serializer

        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data,
                                status=status.HTTP_201_CREATED)

        return JSONResponse(toy_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def toy_detail(request, pk):
    try:
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # $ http :8000/toys/1
        # $ curl -iX GET localhost:8000/toys/1
        toy_serializer = ToySerializer(toy)
        return JSONResponse(toy_serializer.data)

    elif request.method == 'PUT':
        # Basically the same as `POST` but with 'pk' to update specific one

        # http PUT :8000/toys/4 \
        #   name="Sokoban" \
        #   description="a mobile game" \
        #   toy_category="Electronics" \
        #   was_included_in_home=false \
        #   release_date="2017-03-12T09:09:00.656665Z"

        # curl -iX PUT -H "Content-Type: application/json"
        #   -d '{"name":"Tombraider","description":"a mobile game",
        #   "toy_category":"Electronics","was_included_in_home":"false",
        #   "release_date":"2016-05-25T01:01:00.652465Z"}' localhost:8000/toys/5
        toy_data = JSONParser().parse(request)
        toy_serializer = ToySerializer(toy, data=toy_data)

        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data)

        return JSONResponse(toy_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
