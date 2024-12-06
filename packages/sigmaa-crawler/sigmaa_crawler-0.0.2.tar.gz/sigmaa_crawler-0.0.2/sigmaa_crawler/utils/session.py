import requests
from pydantic import BaseModel
from bs4 import BeautifulSoup

from sigmaa_crawler.models.user import User

class Session(BaseModel):
    _token = None
    _base_url = "https://uclb.ucaribe.edu.mx/sigmaav2/"

    def __init__(self, user: User) -> None:
        self.credentials = user

    def get_token(self) -> str:
        """
        Permite obtener el token de la página de login del SIGMAA.
        """ 
        try:
            response = requests.get(self._base_url + "sistema/login")
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error al obtener el token: {e}")

        soup = BeautifulSoup(response.text, "html.parser")
        token_element = soup.find("input", {"name": "token"})
        if token_element:
            self._token = token_element.get("value")
            return self._token
        else:
            raise Exception("No se pudo obtener el token")

    def login(self) -> None:
        """
        Permite iniciar sesión en el SIGMAA usando las credenciales del estudiante.
        """
        if not self._token:
            self.get_token()

        payload = {
            "accion": "login",
            "login": self.credentials.matricula,
            "password": self.credentials.contraseña,
            "struts.token.name": "token",
            "token": self._token
        }

        try:
            response = requests.post(self._base_url + "sistema/login", data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error al iniciar sesión: {e}")

        print(response.text)

    def logout(self):
        """
        Permite cerrar sesión en el SIGMAA.
        """
        try:
            response = requests.get(self._base_url + "sistema/loginInicio?acción=logout")
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error al cerrar sesión: {e}")

        return response.text