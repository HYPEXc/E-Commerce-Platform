from django.shortcuts import redirect
import requests
from django.contrib.auth import get_user_model

User = get_user_model()


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        # You would normally call Clerk's API to create a user here.
        clerk_response = requests.post('https://api.clerk.dev/v1/users', data={
            'email': email,
            'username': username,
            # other fields as needed
        })

        if clerk_response.status_code == 201:  # User created successfully
            clerk_data = clerk_response.json()
            # Create a local user model entry
            User.objects.create(
                clerk_id=clerk_data['id'],
                email=email,
                username=username,
            )
            return redirect('login')  # Redirect to login or success page