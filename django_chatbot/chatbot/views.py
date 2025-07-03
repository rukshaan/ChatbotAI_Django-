from django.shortcuts import render
from django.http import JsonResponse
import openai
from openai.error import RateLimitError, InvalidRequestError, AuthenticationError

openai_api_key=''
openai.api_key = openai_api_key


def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response['choices'][0]['message']['content']
    except RateLimitError:
        return "⚠️ Rate limit exceeded. Please try again shortly."

    except AuthenticationError:
        return "❌ Authentication error. Please check your API key."

    except InvalidRequestError as e:
        return f"🚫 Invalid request: {str(e)}"

    except Exception as e:
        return f"❗ Unexpected error: {str(e)}"

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print(message)
        response=ask_openai(message)
        return JsonResponse({'message': message, 'response': response}) 
    return render(request, 'chatbot.html')