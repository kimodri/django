# How CORS and API Auth Happen Under The Hood
Here's a more detailed breakdown of the request flow, including the two types of CORS requests.

### 1\. Simple Requests 🚀

For "simple" requests (e.g., `GET` or `POST` with a specific content type), the flow is exactly as you described.

1.  A browser-based client (e.g., a React app at `my-site.com`) makes a request to a different domain (`my-api.com`).
2.  The **browser automatically adds an `Origin` header** to the request, containing the URL of the calling site (`Origin: https://my-site.com`).
3.  The request arrives at your Django server, which is configured with CORS middleware (e.g., `django-cors-headers`).
4.  The Django middleware checks the `Origin` header against its list of allowed origins.
5.  Your DRF authentication and permissions (e.g., `AllowAny` or `IsAuthenticated`) kick in and handle the request.
6.  The server generates the response.
7.  Before sending the response, the CORS middleware **adds an `Access-Control-Allow-Origin` header** to it, often with the value from the `Origin` header if it's allowed.
8.  The response is sent back to the browser.
9.  The browser receives the response and checks the `Access-Control-Allow-Origin` header.
10. If the header's value allows `my-site.com`, the browser allows the JavaScript to access the response data. If not, it blocks the response and throws a CORS error.

\<br\>

-----

\<br\>

### 2\. Preflighted Requests ✈️

For "complex" requests—such as `PUT`, `DELETE`, `PATCH`, or a request with custom headers (like an `Authorization` token), the browser adds an extra step for security.

1.  A browser-based client makes a complex request (e.g., a `PUT` request with an `Authorization` header).
2.  Instead of sending the actual `PUT` request immediately, the browser first sends a **CORS preflight request** using the HTTP **`OPTIONS`** method. This is a special request to ask the server for permission.
3.  This `OPTIONS` request includes headers like `Access-Control-Request-Method` (e.g., `PUT`) and `Access-Control-Request-Headers` (e.g., `Authorization`).
4.  The server receives this `OPTIONS` request. Its CORS middleware checks the headers to see if it allows `PUT` requests from that origin with an `Authorization` header. **DRF permissions and authentication are not checked at this stage** because no actual data is being requested or sent.
5.  If the server's CORS policy allows it, it responds with a **200 OK** status code and the appropriate CORS headers in the response (`Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`).
6.  The browser receives this preflight response.
7.  If the preflight response indicates that the actual request is permitted, the browser **then sends the original `PUT` request** to the server.
8.  This second request goes through the full server-side process, including DRF's authentication and permissions check.
9.  The server sends back the final response, which also includes the `Access-Control-Allow-Origin` header.

Your summary was spot-on for simple requests. The key takeaway is that for complex requests, **CORS checks happen twice**: once via the preflight `OPTIONS` request and then again with the headers on the final response. In both cases, the browser's CORS check is always the first line of defense before your application's business logic or DRF permissions are ever considered.