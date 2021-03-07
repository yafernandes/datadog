#!/usr/bin/env python3

import json
import sys

import boto3
import uritools
import urllib.request


def ksm_handler(uri, parts):
    try:
        client = boto3.session.Session().client(
            service_name='secretsmanager',
            region_name=parts.authority
        )
        get_secret_value_response = client.get_secret_value(
            SecretId=parts.path[1:])
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)[parts.fragment], None
    except (Exception) as e:
        return None, str(e)

def url_handler(uri, parts):
    try:
        with urllib.request.urlopen(uri) as f:
            return f.read().decode('utf-8'), None
    except (Exception) as e:
        return None, str(e)

schemes = {
    "ksm": ksm_handler,
    "file": url_handler
}

if __name__ == '__main__':
    input = json.loads(sys.stdin.read())

    output = {}
    for uri in input["secrets"]:
        parts = uritools.urisplit(uri)
        if parts.scheme in schemes:
            result = schemes[parts.scheme](uri, parts)
            output[uri] = {
                "value": result[0],
                "error": result[1]
            }
        else:
            output[uri] = {
                "value": None,
                "error": f'Scheme {parts.scheme} is not support.'
            }

    print(json.dumps(output))
