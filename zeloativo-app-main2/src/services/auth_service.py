import requests

API_URL = "http://127.0.0.1:8000"


class AuthService:
    @staticmethod
    def login(email, password):
        r = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
        if r.status_code == 200:
            return r.json()
        raise Exception(r.json().get("detail", "Erro no login"))

    @staticmethod
    def register(email, password, full_name=None, phone=None, role="patient"):
        r = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": full_name,
                "phone": phone,
                "role": role,
            },
        )
        if r.status_code in (200, 201):
            return r.json()

        # Pode vir 202 se seu backend estiver configurado assim; se vier, só devolve o detail
        if r.status_code == 202:
            return {"detail": r.json().get("detail")}

        raise Exception(r.json().get("detail", "Erro no cadastro"))