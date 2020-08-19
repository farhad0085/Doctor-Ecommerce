1. Get username and password from login form
2. now concate like this username:password
3. make this base64 encoded
4. Now send request to /api/token
5. with header Authorization: "Basic base64 encoded string"
6. Now server will give a token, and user id
7. Convert the token to base64 like step 2
    token:
8. Store token and user_id to browser storage
9. Now for every request send this as header.
    Authorization: Basic base64 of step 7
10. Delete the saved data when user logged out
11. Done