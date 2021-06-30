# Ny Volako

Management of personal finance is a daily routine. "Ny Volako" literally translated from Malagasy to English means
"My Finances". It is an API to records your personal finance history. The aim of this project is to demonstrate skills
of developing, testing, securing, and deploying that API to the cloud. In addition to that, this API would require small
changes, and a Front End to be a Minimum Valuable Product.

## Table of Contents
* Project Dependencies
* Local Development
    * Installing the Dependencies
        * Python 3.9
        * Virtual Environment
        * PIP Dependencies
    * Configuring the Database
    * Configuring Auth0
    * Execute Unit Tests
    * Running the Server
* Hosting on Heroku
* API Reference
    * Error Handling
    * Endpoints
    * GET /accounts
    * POST /accounts
    * PATCH /accounts/<int:account_id>
    * DELETE /accounts/<int:account_id>
    * GET /transactions
    * POST /transactions
    * PATCH /transactions/<int:account_id>
    * DELETE /transactions/<int:account_id>
    

## Project Dependencies

The main libraries, framework, and tools used by this API are:

* Python 3.9
* Flask
* SQLAlchemy
* PostgreSQL
* Auth0
* Heroku
* UnitTest

## Local Development

Here are the steps to run the API in a local development environment.

### Installing the Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the
[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps the dependencies
for each project separate and organized. Instructions for setting up a virtual environment can be found in
the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once a virtual environment is up and running, install dependencies by navigating to the root `./` directory of the
source code and running:

```bash
pip install -r requirements.txt
```

This will install all the required packages marked under the `requirements.txt` file.

### Configuring the Database

Ny Volako API is using PostgreSQL. For a quickstart, under PostgreSQL using tool such as pgAdmin, follow the steps
below:

* Create a user 'nyvolako' with a password 'nyvolako'
* Create a database named 'nyvolako' having as owner the user 'nyvolako'
* Create another database named 'nyvolako_test' having also 'nyvolako' as owner
* Make sure that the DB is running on localhost:5432

Should these parameters be changed, update the file `./config.py` accordingly. It has two classes `Config`
and `ConfigTest`. The first one is to start the server in a development environment and the second one is for UnitTest.

### Configuring Auth0

As this API is based on Auth0, it can be tied to a custom Auth0 tenant. To do that:

* Under Auth0
    * Create an account
    * Create an APP
        * Set Application Login URI to `https://127.0.0.1/login`
        * Set Allowed Callback URLs to `https://127.0.0.1/login-results`
        * Set Allowed Logout URLs to `https://127.0.0.1/logout`
    * Create an API
        * Activate `RBAC`
        * Activate `Add Permissions in the Access Token`
        * Add the following permissions to that API - `accounts:get`, `accounts:delete`, `accounts:new`
          , `accounts:update`,
          `transactions:get`, `transactions:delete`, `transactions:new`, `transactions:update`
    * Create the roles
        * add role `Accountant` with all the permissions
        * add role `Secretary` with only `accounts:get`, `transactions:get`, and `transactions:new`
    * Generate test tokens by navigating to the following url (Consider changing the variables)
        * https://`%DOMAIN_NAME%`/authorize?audience=`%API_IDENTIFIER%`&response_type=token&client_id=`%CLIENT_ID%`
          &redirect_uri=https://127.0.0.1/login-results&state=STATE
            * `DOMAIN_NAME` is the address of the Auth0 tenant in form of `****.auth0.com`
            * `API_IDENTIFIER` is the identifier of the API under Auth0
            * `CLIENT_ID` is the identifier of the APP under Auth0
        * Create users as required and assign them a role using Auth0 dashboard
* Under the source code `./`, modify the following files:
    * `./utils/auth.py` - Change the constants AUTH0_DOMAIN and API_AUDIENCE
    * `./test/tokens.py` - Change the tokens with valid ones using the above steps

### Execute unit tests

If needed, update the file `./test/tokens.py` by changing the tokens with valid ones using the above steps under
configuration.

From within the `./` directory first ensure you are working using your created virtual environment.

To execute the full set of tests, run the following command under the `./` directory.

```bash
python -m unittest discover test
```

### Running the Server

From within the `./` directory first ensure you are working using your created virtual environment. To run the server,
execute:

```bash
flask db upgrade
flask run --reload
```

This API is having `wsgi.py` so flask will start the server using that file. The `--reload` flag will detect file
changes and restart the server automatically.

## Hosting on Heroku

In the next bash commands, name_of_your_application refers to the identifier of the API when hosted in Heroku. Here are
the steps to deploy the API:

* Make sure to have `git` installed
* Create an account in Heroku as needed
* Install Heroku CLI following these [instructions](https://devcenter.heroku.com/categories/command-line)
* Log into Heroku CLI using
  ```bash
  heroku login
  ```
* Create the Heroku app
  ```bash
  heroku create name_of_your_application
  ```
  Change name_of_your_app as necessary
* Add PostgreSQL addon for the database
  ```bash
  heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
  ```
* Configure git by running the next command under `./`
  ```bash
  heroku git:remote -a name_of_your_application
  ```
* Then push the source codes to Heroku
  ```bash
  git push heroku HEAD:master
  ```
* Finally, upgrade the DB in Heroku
  ```bash
  heroku run flask db upgrade --app name_of_your_application
  ```
* The API can be troubleshooted with
  ```bash
  heroku logs --app=name_of_your_application --tail
  ```
* Test the hosted API by adjusting the file `./test_live/__init__.py` as needed
    * Change the constant API_URL to the URL given by Heroku
    * Adjust the tests
    * Run the test
    ```bash
    python -m unittest test_live
    ```

# API Reference

* Base URL: At present, without any changes, this API can be
    * run and accessed locally `http://127.0.0.1:5000`
    * or accessed on Heroku `https://ny-volako.herokuapp.com`
* Authentication: The following tokens issued by `kotogasy.eu.auth0.com` can be used
    * accountant role which can call all endpoints - `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBwWmxGaGxKb1V1TU45UEpGQ3k2NCJ9.eyJpc3MiOiJodHRwczovL2tvdG9nYXN5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMTkzNDYyODU4ODA2Mzc0NjM5OSIsImF1ZCI6Imh0dHBzOi8vbnl2b2xha28ubW9kZXJuYW50Lm1nIiwiaWF0IjoxNjI1MDgyMTM3LCJleHAiOjE2MjUxNjg1MzcsImF6cCI6ImZxTEtXV0lmbkt4cmFFbmpjRkNKMFd4eFZWckhvQXllIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhY2NvdW50czpkZWxldGUiLCJhY2NvdW50czpnZXQiLCJhY2NvdW50czpuZXciLCJhY2NvdW50czp1cGRhdGUiLCJ0cmFuc2FjdGlvbnM6ZGVsZXRlIiwidHJhbnNhY3Rpb25zOmdldCIsInRyYW5zYWN0aW9uczpuZXciLCJ0cmFuc2FjdGlvbnM6dXBkYXRlIl19.GlzfqdWVxRVQeQ3viuVcRo6dB2Uo-pH7c-QNoMjJOPfzMvCUXH_u8gKdVr4bRcixY3PkDhIM7JcFHDev2yu3HVDy5Fz0VvdyBNGvuRJjHnfud5eYalysBY2Bkud7s-qavTgYKz7z-l7c0_HnMjqmxiMNK31Ql1K8zEHBSUuaz0pZnYoWr_dl_W78x_9aYR9Iru2UZYjz5MWbAm_QBSKZ2dPuHOzoDDAYRFLfelVoDV4ypuP0kXIZS_CWtKSf8p1z2WT5MCQOJzytiRDuYSIz_25ol0RLsCxPdf5teJ-305EKbVhdTrlMVSyE4So8js-cWpujgYGASujYEGFVYrRFvA`
    * secretary role which can only get a list of transactions, get list of accounts, and post new transaction - `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBwWmxGaGxKb1V1TU45UEpGQ3k2NCJ9.eyJpc3MiOiJodHRwczovL2tvdG9nYXN5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGRiOWE3YjA2MDViMjAwNzJkNjQ1MGYiLCJhdWQiOiJodHRwczovL255dm9sYWtvLm1vZGVybmFudC5tZyIsImlhdCI6MTYyNTA4MTQ3MywiZXhwIjoxNjI1MTY3ODczLCJhenAiOiJmcUxLV1dJZm5LeHJhRW5qY0ZDSjBXeHhWVnJIb0F5ZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWNjb3VudHM6Z2V0IiwidHJhbnNhY3Rpb25zOmdldCIsInRyYW5zYWN0aW9uczpuZXciXX0.boNDu_H-1ikTOnjaZ8l4l-yGvUldtxQTjTLc90abPMn6ytt15VLiohLloPsJtWceWHSvr9UfmFpDj_BjW4D7mAT5GWUd8mH_YX5x_Za3Te9obSswQ2h30b807rQ1TMXYD8h8F8sT4jSxiadHaZTt7XbjZzCtva_rnj8fWP90dg5T7xGurhTSt0DB-T3xX2OaK_SxOl6OPZ_Ll8VF2Cgy4Y1DHsJ35qDWUAAOBWW3shXs11PrDGlpP0NAOokEf0KoFofy_CqxLWl-E2gNH0hMB-vpJjE9fkKws95EXZAM6yLeEY4ZWoy6sV66Cyy-XUFscz9zwzDldd3Xx8gf89KUcA`

## Error handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:

* 400: Bad Request
* 401: Unauthorized
* 403: Forbidden
* 404: Resource Not Found
* 409: Integrity Error
* 422: Not Processable

## Endpoints

* GET /accounts
* POST /accounts
* PATCH /accounts/<int:account_id>
* DELETE /accounts/<int:account_id>
* GET /transactions
* POST /transactions
* PATCH /transactions/<int:account_id>
* DELETE /transactions/<int:account_id>

## GET /accounts

* Fetches an array of accounts
* Request Arguments: None
* Returns:
    * objects: array of accounts
* Sample:
    ```python
    import requests
    response = requests.get(API_URL + '/accounts',
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true,
      "objects": [{"id": 1, "name": "Bank", "type": "asset"},
                  {"id": 2, "name": "Owner 1", "type":  "equity"}]
    }
    ```

## POST /accounts

* Adds new account to the API database
* Request Arguments: These are expected to be a JSON in the request body
    * name: name of the account
    * type: type of the account and the allowed values are `asset`,`expense`, `drawing`,
      `liability`, `revenue`, and `equity`
* Returns: a json indicating that the post was successful
* Sample:
    ```python
    import requests
    response = requests.post(API_URL + '/accounts', json={'name': 'Bank',
                             'type': 'asset'},
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true
    } 
    ```

## PATCH /accounts/<int:account_id>

* Update only the name of an account that exists already in the API database. The type of the account cannot be updated
  as it may lead to unbalanced accounts
* Request Arguments:
    * account_id part of the URL indicates the account to be updated
    * name provided as a JSON in the request body indicates the new name of the account
* Returns: a json indicating that the update was successful
* Sample:
    ```python
    import requests
    response = requests.patch(API_URL + '/accounts/1', json={'name': 'New Bank'},
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true
    } 
    ```

## DELETE /accounts/<int:account_id>

* Deletes a given account. This returns an error if there is at least one movement attached to the account.
* Request Arguments: account_id, part of the URL, which is the id of the account to be deleted.
* Returns: a json indicating that the deleting was successful
* Sample:
    ```python
    import requests
    response = requests.delete(API_URL + '/accounts/1',
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true
    } 
    ```

## GET /transactions

* Fetches a list of all transactions
* Request Arguments: None
* Returns:
    * objects: an array of transactions where each transaction has a list of movements
* Sample:
    ```python
    import requests
    response = requests.get(API_URL + '/transactions',
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
      [{"date": "Tue, 3 June 2021 10:15:23 GMT",
       "description": "Initial funding",
       "movements": [
           {"account_id": 1,
            "amount": 5000},
           {"account_id": 2,
            "amount": 5000}
       ]}, 
       {"date": "Wed, 9 June 2021 20:50:13 GMT",
       "description": "Buying car",
       "movements": [
           {"account_id": 2,
            "amount": -1000},
           {"account_id": 3,
            "amount": 1000}
       ]}
      ]
    ```

## POST /transactions

* Post a new valid transaction to the database. It is valid when:
    * the sum of the amount of its movements equate by following the rule of
    `asset + expense + drawing = liability + revenue + equity`
    * each movement has an amount different from zero
    * each movement is tied to an account that exists
* Request Arguments: a json object in the request body having the following members
    * date - date of the transaction
    * description - description of the transaction
    * movements - an array of movement where each is having an amount different from zero, and an account_id which 
      exists in the database
* Returns: a json indicating that the post was successful
* Sample:
    ```python
    import requests
    new_transaction = {"date": "Wed, 9 June 2021 20:50:13 GMT",
       "description": "Buying car",
       "movements": [
           {"account_id": 2,
            "amount": -1000},
           {"account_id": 3,
            "amount": 1000}
       ]}
    response = requests.post(API_URL + '/transactions', json=new_transaction,
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true
    } 
    ```

## PATCH /transactions/<int:transaction_id>

* Update an existing transaction while keeping its validity. It is valid when:
    * the sum of the amount of its movements equate by following the rule of
    `asset + expense + drawing = liability + revenue + equity`
    * each movement has an amount different from zero
    * each movement is tied to an account that exists
* Request Arguments:
    * transaction_id, part of the URL, which is the id of the transaction to be updated
    * a json object in the request body having the following members
        * date - date of the transaction
        * description - description of the transaction
        * movements - an array of movement where each is having an amount different from zero, and an account_id which 
          exists in the database
* Returns: a json indicating that the patch was successful
* Sample:
    ```python
    import requests
    updated_transaction = {"date": "Thu, 10 June 2021 20:50:13 GMT",
       "description": "Buying car on another date",
       "movements": [
           {"account_id": 2,
            "amount": -1000},
           {"account_id": 3,
            "amount": 1000}
       ]}
    response = requests.patch(API_URL + '/transactions/2', json=updated_transaction,
                             headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true
    }
    ```

## DELETE /transactions/<int:transaction_id>

* Deletes a transaction from the API database including the movements that are linked to it
* Request Arguments: transaction_id, part of the URL, which is the id of the transaction to be deleted
* Returns: a json indicating that the deleting was successful
* Sample:
    ```python
    import requests
    response = requests.delete(API_URL + '/transactions/2',
                               headers={'Authorization': 'bearer ' + TOKEN})
    ```
* Output Sample:
    ```json
    {
      "success": true
    } 
    ```
