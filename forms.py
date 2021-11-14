from typing import Any, Dict, List, Optional, Union

from fastapi.param_functions import Form


class OAuth2PasswordRequestForm:

    def __init__(
        self,
        grant_type: str = Form(None, regex="password"),
        email: str = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


class TaskAddForm:

    def __init__(
        self,
        title: str = Form(...),
        description: str = Form(...),
    ):
        self.title = title
        self.description = description
