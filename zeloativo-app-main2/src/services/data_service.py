import requests
import json
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


class DataService:
    token = None
    TOKEN_FILE = "token.json"

    # ---------------------------
    # TOKEN
    # ---------------------------
    @classmethod
    def unlink_patient(cls, patient_id: str):
        r = requests.delete(
            f"{API_URL}/link/unlink",
            params={"patient_user_id": patient_id},
            headers=cls.headers(),
            timeout=20,
        )
        if r.status_code >= 400:
            return cls._safe_json(r)
        return cls._safe_json(r)
    @classmethod
    def load_token_from_file(cls):
        """Carrega o token do arquivo ao iniciar o app"""
        if os.path.exists(cls.TOKEN_FILE):
            try:
                with open(cls.TOKEN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls.token = data.get("access_token")
                if cls.token:
                    print(f"Token carregado com sucesso: {cls.token[:10]}...")
            except Exception as e:
                print(f"Erro ao ler token.json: {e}")
                cls.token = None

    @classmethod
    def set_token(cls, token):
        cls.token = token
        try:
            with open(cls.TOKEN_FILE, "w", encoding="utf-8") as f:
                json.dump({"access_token": token}, f)
        except Exception as e:
            print(f"Erro ao salvar token.json: {e}")

    @classmethod
    def headers(cls):
        # se quiser, pode comentar esse print depois
        print(f"DEBUG: Enviando token -> {cls.token[:10] + '...' if cls.token else None}")
        h = {"Content-Type": "application/json"}
        if cls.token:
            h["Authorization"] = f"Bearer {cls.token}"
        return h

    @staticmethod
    def _safe_json(resp: requests.Response):
        try:
            return resp.json()
        except Exception:
            return {"detail": resp.text}

    # ---------------------------
    # MEDICAMENTOS
    # ---------------------------
    @classmethod
    def get_medicines(cls, patient_id: str | None = None):
        params = {}
        if patient_id:
            params["patient_id"] = patient_id
        r = requests.get(f"{API_URL}/medicines", headers=cls.headers(), params=params, timeout=20)
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()

    @classmethod
    def add_medicine(cls, medicine: dict):
        r = requests.post(
            f"{API_URL}/medicines",
            json=medicine,
            headers=cls.headers(),
            timeout=20,
        )
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()

    @classmethod
    def update_medicine(cls, medicine_id: str, medicine: dict):
        r = requests.patch(
            f"{API_URL}/medicines/{medicine_id}",
            json=medicine,
            headers=cls.headers(),
            timeout=20,
        )
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()

    @classmethod
    def delete_medicine(cls, medicine_id: str):
        r = requests.delete(
            f"{API_URL}/medicines/{medicine_id}",
            headers=cls.headers(),
            timeout=20,
        )
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()
    @classmethod
    def list_medicines(cls, patient_id: str | None = None):
        return cls.get_medicines(patient_id)

    @classmethod
    def create_medicine(cls, payload: dict):
        return cls.add_medicine(payload)

    # ---------------------------
    # HISTÓRICO
    # ---------------------------
    @classmethod
    def get_week_history(cls, patient_id: str | None = None):
        params = {}
        if patient_id:
            params["patient_id"] = patient_id
        r = requests.get(f"{API_URL}/history/weekly", headers=cls.headers(), params=params, timeout=20)
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()

    @classmethod
    def get_day_history(cls, day: str, patient_id: str | None = None, tz_offset_hours: int = -3):
        params = {"day": day, "tz_offset_hours": tz_offset_hours}
        if patient_id:
            params["patient_id"] = patient_id
        r = requests.get(
            f"{API_URL}/history/day",
            params=params,
            headers=cls.headers(),
            timeout=20,
        )
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()

    # ✅ seu backend não tem POST /history/intakes (ele tem PATCH /history/intakes/{id})
    # então deixei esse método, mas ele provavelmente não será usado:
    @classmethod
    def register_intake(cls, data: dict):
        r = requests.post(
            f"{API_URL}/history/intakes",
            json=data,
            headers=cls.headers(),
            timeout=20,
        )
        if r.status_code >= 400:
            return cls._safe_json(r)
        return r.json()

    # ✅ método certo pro seu backend atual


    # ---------------------------
    # VÍNCULO
    # ---------------------------
    @classmethod
    def generate_link_code(cls):
        r = requests.post(f"{API_URL}/link/code", headers=cls.headers(), timeout=20)
        if r.status_code >= 400:
            return cls._safe_json(r)
        return cls._safe_json(r)

    @classmethod
    def accept_link_code(cls, code: str):
        r = requests.post(
            f"{API_URL}/link/accept",
            json={"code": code},
            headers=cls.headers(),
            timeout=20,
        )
        body = cls._safe_json(r)
        print("ACCEPT LINK:", r.status_code, body)
        return {"status_code": r.status_code, "body": body}

    @classmethod
    def my_links(cls):
        r = requests.get(f"{API_URL}/link/my-links", headers=cls.headers(), timeout=20)
        if r.status_code >= 400:
            return cls._safe_json(r)
        return cls._safe_json(r)
    @classmethod
    def update_intake_status(cls, event_id: str, status: str):
        r = requests.patch(
            f"{API_URL}/intakes/{event_id}",
            json={"status": status},
            headers=cls.headers(),
            timeout=10,
        )
        return r.json()

    @classmethod
    def snooze_intake(cls, event_id: str, minutes: int = 15):
        r = requests.patch(
            f"{API_URL}/intakes/{event_id}/snooze",
            params={"minutes": minutes},
            headers=cls.headers(),
            timeout=10,
        )
        return r.json()