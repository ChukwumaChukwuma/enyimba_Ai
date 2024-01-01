from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import UserQuery
from reinforcement_learning.hidden_strategy import generate_hidden_state_strategy
from reinforcement_learning.language_tree_search import generate_branches
from reinforcement_learning.policy import determine_best_move
from reinforcement_learning.reward import evaluate_reward
from reinforcement_learning.updated_strategy import update_rl_strategy
from reinforcement_learning.value import assess_value

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

        # Process the query through various components
        hidden_state = generate_hidden_state_strategy(query_text)
        language_tree = generate_branches(query_text, hidden_state)
        policy = determine_best_move(language_tree)
        reward = evaluate_reward(policy)
        updated_strategy = update_rl_strategy(reward)
        response_text = assess_value(updated_strategy)

        # Save query and response to the database
        UserQuery.objects.create(query_text=query_text, response_text=response_text)

        # Return response
        return JsonResponse({'response': response_text})

    except Exception as e:
        return JsonResponse({'error': str(e)})
