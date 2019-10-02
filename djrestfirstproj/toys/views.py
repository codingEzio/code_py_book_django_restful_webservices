from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from toys.models import Toy
from toys.serializers import ToySerializer


# This decorator does lots of things for us
#   * specify what HTTP verbs are supported for a view function
#   * handling the PARSER & RENDERER automatically (so we don't have do it in view)
# To put this in a more simple way:
#   * only expose those needed methods, otherwise it'll raise "405 Method Not Allowed"
#   * PARSER            ->  examines the header then determines the right parser
#   * RENDERER/Response ->  now it accepts more than just 'application/json' (text/html ..)
@api_view(['GET', 'POST', 'OPTIONS'])
def toy_list(request):
    if request.method == 'GET':
        # $ http :8000/toys/
        # $ curl -iX GET localhost:8000/toys/
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return Response(toys_serializer.data)

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
        toy_serializer = ToySerializer(data=request.data)

        if toy_serializer.is_valid():
            toy_serializer.save()
            return Response(toy_serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(toy_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'OPTIONS':
        return Response("We havn't implemented this yet!",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE', 'OPTIONS'])
def toy_detail(request, pk):
    try:
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # $ http :8000/toys/1
        # $ curl -iX GET localhost:8000/toys/1
        toy_serializer = ToySerializer(toy)
        return Response(toy_serializer.data)

    elif request.method == 'PUT':
        # Basically the same as `POST` but with 'pk' to update specific one

        # $ http PUT :8000/toys/4 \
        #   name="Sokoban" \
        #   description="a mobile game" \
        #   toy_category="Electronics" \
        #   was_included_in_home=false \
        #   release_date="2017-03-12T09:09:00.656665Z"

        # curl -iX PUT -H "Content-Type: application/json"
        #   -d '{"name":"Tombraider","description":"a mobile game",
        #   "toy_category":"Electronics","was_included_in_home":"false",
        #   "release_date":"2016-05-25T01:01:00.652465Z"}' localhost:8000/toys/5
        toy_serializer = ToySerializer(toy, data=request.data)

        if toy_serializer.is_valid():
            toy_serializer.save()
            return Response(toy_serializer.data)

        return Response(toy_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # $ http DELETE :8000/toys/3
        # $ curl -iX DELETE localhost:8000/toys/3
        toy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # Use this if you just want to update a specific field.
        # Test commands
        #   $ http PUT :8000/toys/4 name='..'
        #   $ curl -iX -H "..json' -d '{"name":".."}' localhost:8000/toys/4
        pass

    elif request.method == 'OPTIONS':
        return Response("We havn't implemented this yet!",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
