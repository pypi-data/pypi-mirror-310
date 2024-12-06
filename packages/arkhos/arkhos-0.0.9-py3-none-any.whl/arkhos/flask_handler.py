import pdb

from arkhos.http import HttpResponse, Request


def create_flask_request_handler(user_flask_app):
    """Returns a function which takes an Arkhos Request, runs it through Flask and returns and Arkhos Response"""
    # from flask import Flask, jsonify, request

    def flask_handler(request: Request):
        client = user_flask_app.test_client()
        # https://github.com/pallets/werkzeug/blob/main/src/werkzeug/test.py#L1058
        # https://werkzeug.palletsprojects.com/en/stable/test/#werkzeug.test.EnvironBuilder
        flask_response = client.open(
            path=request.path,
            # base_url=None
            query_string=request.GET,
            method=request.method,
            headers=request.headers,
            # data=request.body
        )

        response = HttpResponse(
            flask_response.json
            if flask_response.headers.get("content-type") == "application/json"
            else flask_response.data.decode("utf-8"),
            status=flask_response.status_code,
            headers=flask_response.headers,
        )
        return response

    return flask_handler
