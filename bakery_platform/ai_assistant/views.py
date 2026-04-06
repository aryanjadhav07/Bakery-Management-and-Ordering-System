from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def chatbot_view(request):
    if request.method == 'POST':
        question = request.POST.get('question').lower()
        if 'order' in question:
            answer = 'To place an order, go to the products page, select a product, and click "Add to Order".'
        elif 'enroll' in question:
            answer = 'To enroll in a course, go to the courses page, select a course, and click "Enroll".'
        elif 'contact' in question:
            answer = 'You can contact the baker through the chat page.'
        else:
            answer = "I'm sorry, I don't understand that question."
        return JsonResponse({'answer': answer})
    return render(request, 'ai_assistant/chatbot.html')
