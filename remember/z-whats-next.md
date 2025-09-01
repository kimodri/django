# Conclusion
The book only scratched the surface 😊.

Please read the Django Rest Framework [documentation](https://www.django-rest-framework.org/)

## Advanced Topics worth exploring
1. [Pagination](https://www.django-rest-framework.org/api-guide/pagination/): helpful way to control how data is displayed on individual endpoints
2. [Filtering](https://www.django-rest-framework.org/api-guide/filtering/): necessary in many projects especially in conjunction with the excellent [django-filter](https://github.com/carltongibson/django-filter) library
3. [Throttling](https://www.django-rest-framework.org/api-guide/throttling/): necessary on APIs as a more advanced form of permissions. For example, the public-facing side of the API might have restrictive limits for unauthenticated requests while authenticated requests face much more lenient throttling
4. [caching](https://www.django-rest-framework.org/api-guide/caching/): of the API for performance reasons

## Next Steps
- Implement the pastebin API [here](http://www.django-rest-framework.org/tutorial/1-serialization/)
- A complete listing can be found at [Django Packages](https://djangopackages.org/) or a curated list on the [awesome-django](https://github.com/wsvincent/awesome-django) repo on Github
- The best way to learn is to work backwards from a big project and figure out the pieces along the way