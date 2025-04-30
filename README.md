Система цифрового підпису зображень RSA

 Вимоги до системи
- Python 3.8 або новішої версії
- Бібліотеки:
  - `cryptography` (для роботи з RSA)
  - `pillow` (для обробки зображень)
  - `numpy` (для роботи з пікселями)

Встановити всі необхідні бібліотеки можна командою:
```bash
pip install cryptography pillow numpy
```

 Інструкція з використання

1. Підготовка ключів
Ключі були згенеровані за допомогою OpenSSL у PowerShell:
```powershell
openssl genpkey -algorithm RSA -out keys/private_key.pem -pkeyopt rsa_keygen_bits:4096
openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem
```

2. Підпис зображення
Для підпису PNG-зображення виконайте:
```bash
python sign_image.py шлях/до/зображення.png --output шлях/для/підписаного/зображення.png
```

Приклад:
```bash
python sign_image.py images/original.png --output images/signed.png
```

3. Перевірка підпису
Для перевірки цілісності зображення:
```bash
python verify_image.py шлях/до/підписаного/зображення.png
```

Приклад:
```bash
python verify_image.py images/signed.png
```

 Технічні особливості

Алгоритм роботи
- Підписування:
  1. Обчислюється SHA-256 хеш зображення
  2. Хеш підписується приватним ключем RSA-4096
  3. Підпис вбудовується після маркера IEND у файлі PNG

- Перевірка:
  1. Витягується підпис із зображення
  2. Обчислюється хеш зображення
  3. Перевіряється валідність підпису

 Важливі зауваження
- Приватний ключ (private_key.pem) має бути захищений і не поширюватися
- Для нових проектів можна згенерувати нову пару ключів
- Система працює лише з PNG-зображеннями


