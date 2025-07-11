from fastapi import Request

def get_current_role(request: Request):
    # Try to get role from query param or header, default to 'me'
    role = request.query_params.get('role') or request.headers.get('X-User-Role')
    return role or 'me'