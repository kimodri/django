# Transitioning to Django Being REST API
## For authentication and CSRF
In a decoupled architecture where React handles the front end, you won't use Django's traditional `LoginView` or the `{% csrf_token %}` template tag. These features are designed for Django's server-side rendering, where the backend generates and serves HTML pages.

For a React application, the interaction with your Django backend is entirely through **API calls**. Therefore, you use Django's API-specific counterparts to handle these critical functions.

***

## API Authentication (No `LoginView`)

Instead of Django's `LoginView`, which renders a login form, you will create an API endpoint that handles authentication requests. The most common approach is **Token-based Authentication**.

1.  **React sends credentials**: Your React component sends a `POST` request to a Django API endpoint (e.g., `/api/login/`), providing the user's username and password in the request body (as JSON).
2.  **Django verifies and returns a token**: The Django backend receives this request, verifies the credentials, and if they are valid, it generates a unique **authentication token** for that user. This token is then returned to the React front end in the API response.
3.  **React stores the token**: React saves this token, often in local storage or an in-memory variable, to use for subsequent authenticated requests.
4.  **Token is used for protected routes**: For any API call that requires a logged-in user (e.g., fetching profile data, creating a post), React includes the token in the request headers, usually in the `Authorization` header. Django REST Framework then uses this token to identify the user and grant access. 

This is a much more secure and stateless approach for APIs than using Django's session-based authentication.

***

## CSRF Protection (No `{% csrf_token %}`)

The `{% csrf_token %}` template tag works by embedding a token directly into an HTML form. Since your React app doesn't receive these forms from Django, that tag becomes irrelevant. However, CSRF protection is still crucial.

Django REST Framework handles CSRF in two ways, depending on your authentication method:

* **Token-based Authentication (Recommended)**: For this approach, you are not vulnerable to classic CSRF attacks. Since each request is authenticated with a unique token sent in the header (not a cookie that the browser automatically sends), a malicious third-party site cannot trick a user into making a valid request. Therefore, you do **not need to send a CSRF token** with your requests.

* **Session-based Authentication**: If you still decide to use Django's session authentication for your API (e.g., for testing or within a single-domain app), you would need to get the CSRF token from a cookie that Django sets and manually include it in your AJAX requests from React.

In summary, for a typical Django + React setup, you'll rely on the **Django REST Framework** to provide a **token-based authentication API** and will not use Django's traditional `LoginView` or the `{% csrf_token %}` template tag.

Authentication in a blog site where Django is the backend API and React is the front end typically uses **token-based authentication**. The process involves the React app sending user credentials to Django, which then returns a unique token. The React app then uses this token for all subsequent requests to access protected data.

Here's a step-by-step guide on how it works, with class-based views and code snippets.

-----
# Django React Authentication Sample

## Step 1: Django Backend Setup ⚙️

First, you need to install Django REST Framework and configure it to use token authentication.

### **Install necessary packages:**

```bash
pip install djangorestframework
pip install drf-authtoken
```

### **Update `settings.py`:**

Add `rest_framework` and `rest_framework.authtoken` to your `INSTALLED_APPS`. Then, set the default authentication class to `TokenAuthentication`.

```python
# settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken', # Add this line
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

Now, run migrations to create the `authtoken_token` table in your database.

```bash
python manage.py migrate
```

-----

## Step 2: Backend Login View (`views.py`) 🔐

You'll create a class-based view to handle the login request. We'll use Django REST Framework's `ObtainAuthToken` view and override its behavior slightly to return more user data.

```python
# blog_app/views.py

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
```

### **Explanation:**

  * This class inherits from DRF's `ObtainAuthToken`, which handles validating the username and password for you.
  * The `post` method is overridden to return not just the token, but also the user's ID and username, which can be useful for the front end.

-----

## Step 3: Backend URLs (`urls.py`)

Create a URL endpoint that points to your new custom login view.

```python
# blog_site/urls.py

from django.urls import path
from blog_app.views import CustomAuthToken

urlpatterns = [
    path('api/login/', CustomAuthToken.as_view(), name='api-login'),
    ...
]
```

-----

## Step 4: Frontend Login (React Component) 💻

The React component will make a `POST` request to your Django login endpoint. It will then store the returned token for later use.

```javascript
// Login.js (React Component)

import React, { useState } from 'react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      localStorage.setItem('authToken', data.token); // Store the token
      console.log('Login successful! Token:', data.token);
      // Redirect or update UI to show logged-in state
      
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input 
        type="text" 
        placeholder="Username" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)} 
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
      />
      <button type="submit">Log In</button>
    </form>
  );
};

export default Login;
```

-----

## Step 5: Accessing Protected Data 🔒

Now, when you want to access a protected blog post or other user-specific data, your React component will retrieve the stored token and include it in the `Authorization` header of the request.

```javascript
// ProtectedRoute.js (React Component)

import React, { useEffect, useState } from 'react';

const BlogPostList = () => {
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    const fetchPosts = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No authentication token found.');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/blogposts/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`, // Pass the token here
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch posts.');
        }

        const data = await response.json();
        setPosts(data);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
};

export default BlogPostList;
```

-----

## Step 6: Backend Protection of Views 🛡️

Finally, on the Django side, you'll protect your views by using the `IsAuthenticated` permission class. This tells DRF that a valid authentication token must be provided in the request headers to access this view.

```python
# blog_app/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated] 
```