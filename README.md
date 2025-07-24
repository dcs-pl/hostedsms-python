HostedSMS API
================

API dla usługi wysyłki SMS - HostedSMS.pl

Opis WebService dostępny jest pod adresem https://api.hostedsms.pl/WS/smssender.asmx


# 📤 HostedSMS – Przykład użycia API

Ten przykład pokazuje, jak korzystać z klasy `HostedSMSApi`, aby wysyłać wiadomości SMS do jednego lub wielu odbiorców.

---

## 🔧 Konfiguracja

Uzupełnij dane dostępowe oraz numery docelowe:

```python
from hostedsms.api import HostedSMSApi

HOSTED_SMS_USER = "<your_username>"
HOSTED_SMS_PASSWORD = "<your_password>"
HOSTED_SMS_SENDER = "<your_sender_id>"

SEND_TO_NUMBER = "<recipient_number_1>"
SEND_TO_OTHER_NUMBER = "<recipient_number_2>"
```

---

## 🔁 Generowanie `transaction_id`

```python
import random
import string

def get_transaction_id():
    chars = string.ascii_letters + string.digits
    transaction_id = "".join(random.choice(chars) for _ in range(20))
    print("transaction_id:", transaction_id)
    return transaction_id
```

---

## 📨 Wysyłanie pojedynczego SMS-a

```python
api = HostedSMSApi(HOSTED_SMS_USER, HOSTED_SMS_PASSWORD)

print("Sending an SMS message")
api.send_sms(
    phone=SEND_TO_NUMBER,
    message="Hello!",
    transaction_id=get_transaction_id(),
    priority=3,
    sender=HOSTED_SMS_SENDER,
)
```

---

## 📨 Wysyłanie wiadomości do wielu odbiorców

```python
print("Sending a message with send_smses")
api.send_smses(
    phones=[SEND_TO_NUMBER, SEND_TO_OTHER_NUMBER],
    message="Hello from send_smses!",
    transaction_id=get_transaction_id(),
    priority=3,
    sender=HOSTED_SMS_SENDER,
)
```

---

## ✅ Uwagi

- Funkcja `get_transaction_id()` generuje unikalny ID transakcji dla śledzenia wiadomości.
- Upewnij się, że dane logowania i numery telefonów są prawidłowe.
- Funkcje `send_sms` i `send_smses` mogą mieć różne wymagania zależnie od implementacji API.
