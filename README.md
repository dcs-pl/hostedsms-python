HostedSMS API
================

API dla usługi wysyłki SMS - HostedSMS.pl

Opis WebService dostępny jest pod adresem https://api.hostedsms.pl/WS/smssender.asmx
Opis metod API jest dostepny pod adresem https://hostedsms.pl/pl/api-sms/opis-techniczny-api


## 📤 HostedSMS – Przykład użycia API

Ten przykład pokazuje, jak korzystać z klasy `HostedSMSApi`, aby wysyłać wiadomości SMS do jednego lub wielu odbiorców.

### 🔧 Konfiguracja

Uzupełnij dane dostępowe oraz numery docelowe:

```python
from hostedsms.api import HostedSMSApi

HOSTED_SMS_USER = "<your_username>"
HOSTED_SMS_PASSWORD = "<your_password>"
HOSTED_SMS_SENDER = "<your_sender_id>"

SEND_TO_NUMBER = "<recipient_number_1>"
SEND_TO_OTHER_NUMBER = "<recipient_number_2>"
```

### 🔁 Generowanie `transaction_id`

```python
api = HostedSMSApi(HOSTED_SMS_USER, HOSTED_SMS_PASSWORD)

transaction_id = api.get_transaction_id()
```

### 📨 Wysyłanie pojedynczego SMS-a

```python
api = HostedSMSApi(HOSTED_SMS_USER, HOSTED_SMS_PASSWORD)

print("Sending an SMS message")
api.send_sms(
    phone=SEND_TO_NUMBER,
    message="Hello!",
    transaction_id=api.get_transaction_id(),
    priority=3,
    sender=HOSTED_SMS_SENDER,
)
```

### 📨 Wysyłanie wiadomości do wielu odbiorców

```python
print("Sending a message with send_smses")
api.send_smses(
    phones=[SEND_TO_NUMBER, SEND_TO_OTHER_NUMBER],
    message="Hello from send_smses!",
    transaction_id=api.get_transaction_id(),
    priority=3,
    sender=HOSTED_SMS_SENDER,
)
```

### ⬆️ Pobieranie odebranych SMS-ów dla danego odbiorcy

```python
import datetime

RECIPIENT_NUMBER = "<recipient_phone_number_1>"
GET_INPUT_FROM_DATETIME = datetime.datetime(2000, 1, 1)
GET_INPUT_TO_DATETIME = datetime.datetime.now()

print("Getting input SMS messages with get_input_smses")
response = api.get_input_smses(
    _from=GET_INPUT_FROM_DATETIME,
    to=GET_INPUT_TO_DATETIME,
    recipient=RECIPIENT_NUMBER,
)
print("Received results: " + str(response.input_sms))
```


### ✅ Uwagi

- Funkcja `get_transaction_id()` generuje unikalny ID transakcji dla śledzenia wiadomości.
- Upewnij się, że dane logowania i numery telefonów są prawidłowe. Powinny być podawane w postaci międzynarodowej, np. 48xxxxxxxxx.
- Pola funkcji `send_sms` i `send_smses` mogą mieć różną opcjonalność zależnie od implementacji API.
- Pole `priority` akceptuje wartości całkowite z zakresu [0; 3], gdzie 3 to najwyższy priorytet.
