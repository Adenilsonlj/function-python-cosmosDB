import json
import logging
import azure.functions as func
from.commands import get_all
from.commands import create_item
from.commands import delete_item
from.commands import upsert_item


def main(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method

    if method == 'GET':
        return func.HttpResponse(
            get_all(),
            mimetype='json',
            status_code=200
        )

    elif method == 'POST':
        req_body = req.get_json()
        create_item(req_body.get('firstname'), req_body.get('age'))
        return func.HttpResponse(
            'Success!!',
            status_code=200
        )

    elif method == 'DELETE':
        id = req.params.get('id')
        firstname = req.params.get('firstname')
        delete_item(id, firstname)
        return func.HttpResponse(
            'Success!!',
            status_code=200
        )

    elif method == 'PUT':
        req_body = req.get_json()
        upsert_item(req_body.get('id'), req_body.get(
            'firstname'), req_body.get('age'))
        return func.HttpResponse(
            'Success!!',
            status_code=200
        )
