# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import UserQuery
from reinforcement_learning.policy import determine_best_move

@require_http_methods(["GET"])
def get_user_query_view(request):
    try:
        # Fetch the latest user query from your database
        latest_query = UserQuery.objects.latest('id')
        return JsonResponse({'query': latest_query.query_text})
    except UserQuery.DoesNotExist:
        return JsonResponse({'error': 'No queries found'}, status=404)


@require_http_methods(["POST"])
def chatbot_response(request):
    try:
        # Extract query from request
        query_text = request.POST.get('query')

        # Process the query to determine the best move
        best_move_result = determine_best_move(query_text)

        # Save query and response to the database
        UserQuery.objects.create(query_text=query_text, response_text=best_move_result['best_move'])

        # Return response
        return JsonResponse({'response': best_move_result['best_move']})

    except Exception as e:
        return JsonResponse({'error': str(e)})
