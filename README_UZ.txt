AI Telegram Bot Yaratuvchi — boshlang‘ich loyiha

MUHIM:
Bu tayyor boshlang‘ich kod, lekin internetga joylangan va 24/7 ishlayotgan bot emas.
Uni ishga tushirish uchun Python 3.11+ va hosting/server kerak.

1. @BotFather orqali asosiy bot yarating.
2. Tokenni .env.example faylidagi MAKER_BOT_TOKEN qiymatiga qo‘ying (fayl nomini .env qiling).
3. Terminalda:
   pip install -r requirements.txt
   python bot.py

XAVFSIZLIK:
- Asosiy bot tokenini ommaga yubormang yoki GitHub’ga yuklamang.
- Demo foydalanuvchi tokenlarini faylga saqlamaydi va logga chiqarmaydi.
- BotFather tokenini chatga yuborish xavf tug‘diradi; production uchun tokenlarni shifrlangan saqlash, egasini tekshirish, rate-limit va tokenni o‘chirish funksiyasi kerak.

CHEKLOV:
Hozirgi demo tokenni tekshiradi va foydalanuvchi g‘oyasini qabul qiladi. U yangi botni avtomatik yaratib, doimiy ishlatadigan to‘liq tizim emas. Buning uchun hostingda alohida bot-worker, persistent database va har bir bot uchun ishga tushirish/boshqarish mexanizmi qo‘shilishi lozim. Har qanday g‘oyadan cheksiz bot yaratish uchun esa AI API va xavfsizlik nazorati ham kerak.
