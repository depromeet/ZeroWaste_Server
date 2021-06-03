def build_response_body(data, error_code=0):
    return {
        'error_code': error_code,
        'data': data
    }
