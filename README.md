# Task-1
Here using mogodb atlas we create a user model:
[name, 
email,
phone,
api_key, 
api_secret_key,
access_token, 
token_expiry_time,
token_updated_at]
And
->Every day we check if access_token is expired or not,
->if its expired we generate a new token(access_token)
->Later update the token_updated_at, and token_expiry_time for the same.
