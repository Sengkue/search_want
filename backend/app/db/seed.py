from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.permissions import ROLE_SHOP_OWNER, ROLE_SUPER_ADMIN, ROLE_USER
from app.core.security import hash_password, verify_password
from app.db.models import Category, Notification, ProblemKeyword, Shop, User

DEMO_ACCOUNT_DEFAULTS: dict[str, tuple[str, str, str, str]] = {
    "admin@searchwant.com": ("admin123", "ຜູ້ດູແລລະບົບ", "+856 20 5500 0001", ROLE_SUPER_ADMIN),
    "owner@searchwant.com": ("owner123", "ສົມໃຈ ເຈົ້າຂອງອູ່ລົດ", "+856 20 5560 1230", ROLE_SHOP_OWNER),
    "user@searchwant.com": ("user123", "ບຸນມີ ຄົນຂັບລົດ", "+856 20 5911 2233", ROLE_USER),
}

# Default map center: Vientiane, Laos
DEFAULT_CENTER_LAT = 17.9757
DEFAULT_CENTER_LNG = 102.6331
DEFAULT_AREA_NAME = "ວຽງຈັນ"


CATEGORIES_DATA = [
    {
        "name": "ສ້ອມແປງລົດ ແລະ ອູ່ລົດ",
        "slug": "car-auto-repair",
        "icon": "mdi-car-wrench",
        "color": "#1E88E5",
        "description": "ຊ່າງສ້ອມແປງລົດທົ່ວໄປ, ກວດເຊັກເຄື່ອງຈັກ, ເບກ, ເກຍ, ໝໍ້ນ້ຳ ແລະ ນ້ຳມັນຮົ່ວ.",
    },
    {
        "name": "ລົດລາກ ແລະ ຊ່ວຍເຫຼືອສຸກເສີນ",
        "slug": "towing-roadside",
        "icon": "mdi-tow-truck",
        "color": "#E53935",
        "description": "ບໍລິການລົດລາກ 24 ຊົ່ວໂມງ, ຊ່ວຍເຫຼືອລົດເສຍກາງທາງ ແລະ ເປີດລັອກລົດ.",
    },
    {
        "name": "ຢາງລົດ ແລະ ແບັດເຕີຣີ້",
        "slug": "tire-battery",
        "icon": "mdi-car-tire-alert",
        "color": "#FB8C00",
        "description": "ປະຢາງລົດແບນ, ປ່ຽນລໍ້, ກະຕຸ້ນແບັດເຕີຣີ້ ແລະ ສົ່ງແບັດເຕີຣີ້ລົດໃໝ່.",
    },
    {
        "name": "ສ້ອມແປງລົດຈັກ",
        "slug": "motorcycle-repair",
        "icon": "mdi-motorbike",
        "color": "#8E24AA",
        "description": "ສ້ອມເຄື່ອງຈັກລົດຈັກ, ປ່ຽນໂສ້/ສາຍແອວ, ປະຢາງ ແລະ ສ້ອມລະບົບໄຟຟ້າ.",
    },
    {
        "name": "ສ້ອມໂທລະສັບ ແລະ ຄອມພິວເຕີ",
        "slug": "phone-computer",
        "icon": "mdi-cellphone-cog",
        "color": "#00897B",
        "description": "ປ່ຽນໜ້າຈໍແຕກ, ກູ້ເຄື່ອງຕົກນ້ຳ, ສ້ອມແລັບທັອບ ແລະ ປ່ຽນແບັດເຕີຣີ້.",
    },
    {
        "name": "ປະປາ ແລະ ລະບົບນ້ຳໃນເຮືອນ",
        "slug": "home-plumbing",
        "icon": "mdi-pipe-wrench",
        "color": "#039BE5",
        "description": "ທໍ່ນ້ຳແຕກ, ກ໊ອກນ້ຳຮົ່ວ, ທໍ່ລະບາຍນ້ຳຕັນ, ປັ໊ມນ້ຳ ແລະ ສ້ອມແປງຫ້ອງນ້ຳ.",
    },
    {
        "name": "ໄຟຟ້າ ແລະ ສ້ອມແອເຢັນ",
        "slug": "electrical-ac",
        "icon": "mdi-air-conditioner",
        "color": "#43A047",
        "description": "ແອເຢັນບໍ່ເຢັນ, ເຕີມແກັສ, ໄຟຟ້າດັບໃນເຮືອນ ແລະ ກວດສາຍໄຟເພື່ອຄວາມປອດໄພ.",
    },
    {
        "name": "ຄລີນິກ ແລະ ຮ້ານຂາຍຢາ",
        "slug": "clinic-pharmacy",
        "icon": "mdi-medical-bag",
        "color": "#D81B60",
        "description": "ຮ້ານຂາຍຢາໃກ້ຄຽງ, ອຸປະກອນປະຖົມພະຍາບານ, ຄລີນິກສຸກເສີນ ແລະ ປິ່ນປົວບາດແຜນ້ອຍ.",
    },
]


# (category slug, [keywords in Lao + English], symptom label, advice hint)
# Keywords are matched as substrings of the user's text, so both Lao and English phrases work.
KEYWORDS_DATA: list[tuple[str, list[str], str, str]] = [
    # ສ້ອມແປງລົດ
    ("car-auto-repair", ["car", "ລົດເສຍ", "ລົດມີບັນຫາ"], "ລົດມີບັນຫາທົ່ວໄປ",
     "ເປີດໄຟສຸກເສີນຖ້າຈອດໃກ້ຖະໜົນ. ອູ່ສ້ອມລົດໃກ້ຄຽງສາມາດກວດ ແລະ ວິເຄາະບັນຫາທີ່ທ່ານບໍ່ຮູ້ສາເຫດໃຫ້ໄດ້."),
    ("car-auto-repair", ["won't start", "ລົດສະຕາດບໍ່ຕິດ", "ສະຕາດບໍ່ຕິດ", "ລົດບໍ່ຕິດ"], "ລົດສະຕາດບໍ່ຕິດ / ຈູດເຄື່ອງບໍ່ໄດ້",
     "ກວດເບິ່ງວ່າໄຟໜ້າປັດຕິດບໍ. ຖ້າມີສຽງກົດດັງຕິກໆ ມັກແມ່ນແບັດເຕີຣີ້ອ່ອນ ຫຼື ໄດສະຕາດເສຍ; ຖ້າໝູນແຕ່ບໍ່ຕິດ ມັກແມ່ນລະບົບນ້ຳມັນ/ໄຟຈູດ."),
    ("car-auto-repair", ["engine", "ເຄື່ອງຈັກ", "ໄຟເຕືອນເຄື່ອງຈັກ"], "ເຄື່ອງຈັກມີບັນຫາ / ໄຟເຕືອນເຄື່ອງຈັກ",
     "ຫຼີກລ່ຽງການຂັບດ້ວຍຄວາມໄວຮອບສູງ. ໃຫ້ຊ່າງໃກ້ຄຽງເຊື່ອມເຄື່ອງສະແກນ OBD-II ເພື່ອກວດວິເຄາະ."),
    ("car-auto-repair", ["smoke", "ມີຄວັນ", "ຄວັນ"], "ມີຄວັນ ຫຼື ເຄື່ອງຮ້ອນເກີນ",
     "ຈອດລົດຢ່າງປອດໄພ ແລ້ວດັບເຄື່ອງທັນທີ. ຢ່າເປີດຝາໝໍ້ນ້ຳຕອນຍັງຮ້ອນ — ລໍຖ້າຢ່າງໜ້ອຍ 30 ນາທີ."),
    ("car-auto-repair", ["overheat", "ຮ້ອນເກີນ", "ເຄື່ອງຮ້ອນ", "ໝໍ້ນ້ຳຮ້ອນ"], "ເຄື່ອງຍົນຮ້ອນເກີນ",
     "ປິດແອ, ຈອດລົດຢ່າງປອດໄພ ແລະ ດັບເຄື່ອງ ເພື່ອບໍ່ໃຫ້ຝາສູບເສຍຫາຍ."),
    ("car-auto-repair", ["brake", "ເບກ"], "ເບກມີສຽງດັງ ຫຼື ເບກອ່ອນ",
     "ຂັບຊ້າໆ ຫຼື ເອີ້ນລົດລາກຖ້າຮູ້ສຶກວ່າເບກບໍ່ປອດໄພ. ໃຫ້ກວດຜ້າເບກ ແລະ ນ້ຳມັນເບກທັນທີ."),
    ("car-auto-repair", ["noise", "ສຽງດັງ", "ສຽງແປກ"], "ມີສຽງດັງແປກໆ / ສຽງກະທົບ",
     "ສັງເກດວ່າສຽງເກີດຕອນເບກ, ຕອນເລ້ຽວ ຫຼື ຕອນຈອດຕິດເຄື່ອງ — ຈະຊ່ວຍໃຫ້ຊ່າງຫາສາເຫດໄດ້ໄວຂຶ້ນ."),
    ("car-auto-repair", ["oil", "ນ້ຳມັນຮົ່ວ", "ນ້ຳມັນເຄື່ອງ"], "ນ້ຳມັນ ຫຼື ຂອງແຫຼວຮົ່ວໃຕ້ລົດ",
     "ກວດລະດັບນ້ຳມັນເຄື່ອງກ່ອນສະຕາດ; ຖ້ານ້ຳມັນຂາດ ເຄື່ອງຈັກອາດຈະຕິດຕາຍ."),
    # ລົດລາກ
    # A car that won't start is often a dead battery or needs towing, so these categories
    # also match it (same symptom label/advice as the main entry above, so it is not duplicated).
    ("tire-battery", ["won't start", "ລົດສະຕາດບໍ່ຕິດ", "ສະຕາດບໍ່ຕິດ", "ລົດບໍ່ຕິດ"], "ລົດສະຕາດບໍ່ຕິດ / ຈູດເຄື່ອງບໍ່ໄດ້",
     "ກວດເບິ່ງວ່າໄຟໜ້າປັດຕິດບໍ. ຖ້າມີສຽງກົດດັງຕິກໆ ມັກແມ່ນແບັດເຕີຣີ້ອ່ອນ ຫຼື ໄດສະຕາດເສຍ; ຖ້າໝູນແຕ່ບໍ່ຕິດ ມັກແມ່ນລະບົບນ້ຳມັນ/ໄຟຈູດ."),
    ("towing-roadside", ["won't start", "ລົດສະຕາດບໍ່ຕິດ", "ສະຕາດບໍ່ຕິດ", "ລົດບໍ່ຕິດ"], "ລົດສະຕາດບໍ່ຕິດ / ຈູດເຄື່ອງບໍ່ໄດ້",
     "ກວດເບິ່ງວ່າໄຟໜ້າປັດຕິດບໍ. ຖ້າມີສຽງກົດດັງຕິກໆ ມັກແມ່ນແບັດເຕີຣີ້ອ່ອນ ຫຼື ໄດສະຕາດເສຍ; ຖ້າໝູນແຕ່ບໍ່ຕິດ ມັກແມ່ນລະບົບນ້ຳມັນ/ໄຟຈູດ."),
    ("towing-roadside", ["tow", "ລົດລາກ", "ລາກລົດ"], "ຕ້ອງການລົດລາກສຸກເສີນ",
     "ຢູ່ໃນບ່ອນປອດໄພຫ່າງຈາກເລນລົດ ແລະ ສົ່ງຈຸດ GPS ຂອງທ່ານໃຫ້ຜູ້ໃຫ້ບໍລິການລົດລາກ."),
    ("towing-roadside", ["stuck", "ລົດຕິດ", "ຕິດຢູ່ກາງທາງ"], "ລົດຕິດ / ເສຍກາງທາງ",
     "ເປີດໄຟສຸກເສີນ ແລ້ວຕິດຕໍ່ບໍລິການກູ້ໄພ ຫຼື ລົດລາກ 24 ຊົ່ວໂມງໃກ້ຄຽງ."),
    ("towing-roadside", ["breakdown", "ເສຍກາງທາງ", "ລົດເສຍກາງທາງ"], "ລົດເສຍກາງທາງ",
     "ຂັບເຂົ້າຂ້າງທາງຖ້າເຮັດໄດ້ ແລ້ວໂທຫາບໍລິການຊ່ວຍເຫຼືອກາງທາງ ຫຼື ອູ່ລົດໃກ້ຄຽງ."),
    ("towing-roadside", ["accident", "ອຸບັດເຫດ", "ຊົນກັນ"], "ເກີດອຸບັດເຫດ / ລົດຂັບຕໍ່ບໍ່ໄດ້",
     "ໃຫ້ແນ່ໃຈວ່າທຸກຄົນປອດໄພກ່ອນ, ຖ່າຍຮູບສະຖານທີ່ ແລ້ວຈັດລົດລາກໄປອູ່ສ້ອມທີ່ເຊື່ອຖືໄດ້."),
    # ຢາງ ແລະ ແບັດເຕີຣີ້
    ("tire-battery", ["tire", "ຢາງລົດ", "ຢາງແຕກ", "ຢາງຮົ່ວ"], "ຢາງລົດແບນ ຫຼື ຖືກແທງ",
     "ຢ່າຂັບຕໍ່ໃນຂະນະຢາງແບນ — ຈະເຮັດໃຫ້ກະທະລໍ້ ແລະ ແກ້ມຢາງເສຍຫາຍ. ຮ້ານປະຢາງເຄື່ອນທີ່ ຫຼື ຮ້ານໃກ້ຄຽງສາມາດປະ ຫຼື ປ່ຽນໃຫ້ໄດ້."),
    ("tire-battery", ["flat", "ຢາງແບນ", "ລົມອ່ອນ"], "ຢາງແບນ / ລົມຢາງອ່ອນ",
     "ຈອດລົດເທິງພື້ນຮາບຫ່າງຈາກລົດອື່ນ ກ່ອນປ່ຽນຢາງອາໄຫຼ່ ຫຼື ໂທຫາຮ້ານຢາງໃກ້ຄຽງ."),
    ("tire-battery", ["battery", "ແບັດເຕີຣີ້", "ແບັດ", "ໝໍ້ໄຟລົດ"], "ແບັດເຕີຣີ້ລົດໝົດ / ຕ້ອງກະຕຸ້ນແບັດ",
     "ຖ້າໄຟໜ້າລົດມືດ ຫຼື ມີສຽງຕິກໆ ຕອນບິດກຸນແຈ ມັກແມ່ນແບັດເຕີຣີ້ໝົດ."),
    ("tire-battery", ["jump", "ກະຕຸ້ນແບັດ", "ພ່ວງແບັດ"], "ຕ້ອງການກະຕຸ້ນແບັດເຕີຣີ້",
     "ຢ່າໃຫ້ສາຍພ່ວງແບັດຢູ່ໃກ້ສາຍພານພັດລົມທີ່ກຳລັງໝູນ ແລະ ຕໍ່ຂົ້ວບວກ (+) ກ່ອນສະເໝີ."),
    # ລົດຈັກ
    ("motorcycle-repair", ["motorbike", "ລົດຈັກ", "ມໍເຕີໄຊ"], "ລົດຈັກເສຍ",
     "ເຂັນລົດຈັກຂຶ້ນຂ້າງທາງທີ່ປອດໄພ; ຊ່າງລົດຈັກໃກ້ຄຽງແກ້ໄຂສາຍແອວ, ຢາງ ແລະ ຫົວທຽນໄດ້."),
    ("motorcycle-repair", ["scooter", "ສະກູດເຕີ", "ລົດຈັກອັດຕະໂນມັດ"], "ສະກູດເຕີສະຕາດບໍ່ຕິດ / ສາຍແອວມີບັນຫາ",
     "ກວດສະວິດດັບເຄື່ອງ ແລະ ເຊັນເຊີຂາຕັ້ງກ່ອນ ຫຼື ແວ່ຮ້ານສ້ອມລົດຈັກໃກ້ຄຽງ."),
    ("motorcycle-repair", ["chain", "ໂສ້ລົດຈັກ", "ໂສ້ຂາດ"], "ໂສ້ລົດຈັກຂາດ ຫຼື ຫຼົມ",
     "ຢ່າຂີ່ຕໍ່ຖ້າໂສ້ຫຼຸດ ເພາະອາດເຮັດໃຫ້ລໍ້ຫຼັງລັອກ."),
    # ໂທລະສັບ ແລະ ຄອມພິວເຕີ
    ("phone-computer", ["phone", "ໂທລະສັບ", "ມືຖື"], "ໂທລະສັບມີບັນຫາ / ເສຍຫາຍ",
     "ສຳຮອງຂໍ້ມູນສຳຄັນກ່ອນ ຖ້າໜ້າຈໍຍັງແຕະໄດ້ ແລ້ວຈຶ່ງນຳໄປສ້ອມ."),
    ("phone-computer", ["screen", "ໜ້າຈໍແຕກ", "ຈໍແຕກ", "ໜ້າຈໍ"], "ໜ້າຈໍແຕກ ຫຼື ດຳມືດ",
     "ຢ່າກົດໜ້າຈໍທີ່ແຕກ; ຊ່າງໃກ້ຄຽງສາມາດປ່ຽນໜ້າຈໍໃຫ້ພາຍໃນ 1–2 ຊົ່ວໂມງ."),
    ("phone-computer", ["laptop", "ແລັບທັອບ", "ຄອມພິວເຕີ"], "ແລັບທັອບ / ຄອມເປີດບໍ່ຕິດ",
     "ຖອດສາຍສາກອອກຖ້ານ້ຳຫົກໃສ່ ແລະ ຢ່າເປີດເຄື່ອງຈົນກວ່າຈະແຫ້ງ ແລະ ໃຫ້ຊ່າງກວດ."),
    # ປະປາ
    ("home-plumbing", ["pipe", "ທໍ່ນ້ຳ", "ທໍ່ແຕກ"], "ທໍ່ນ້ຳແຕກ ຫຼື ຮົ່ວ",
     "ປິດວາວນ້ຳຫຼັກທັນທີເພື່ອບໍ່ໃຫ້ນ້ຳຖ້ວມ ແລ້ວໂທຫາຊ່າງປະປາໃກ້ຄຽງ."),
    ("home-plumbing", ["leak", "ນ້ຳຮົ່ວ"], "ນ້ຳຮົ່ວ / ກ໊ອກນ້ຳຢອດ",
     "ເອົາຖັງຮອງໃຕ້ບ່ອນທີ່ນ້ຳຢອດ ແລະ ປິດວາວນ້ຳຢູ່ໃຕ້ອ່າງລ້າງ/ໂຖສ້ວມ."),
    ("home-plumbing", ["clog", "ທໍ່ຕັນ", "ສ້ວມຕັນ", "ລະບາຍນ້ຳຕັນ"], "ທໍ່ລະບາຍນ້ຳ ຫຼື ສ້ວມຕັນ",
     "ຢ່າເອົານ້ຳຢາລ້າງທໍ່ແຮງໆ ມາປະສົມກັນ ກ່ອນໃຫ້ຊ່າງປະປາໃຊ້ເຄື່ອງແຍງທໍ່."),
    # ໄຟຟ້າ ແລະ ແອ
    ("electrical-ac", ["aircon", "ແອເຢັນ", "ແອບໍ່ເຢັນ"], "ແອເຢັນບໍ່ເຢັນ / ນ້ຳຮົ່ວ",
     "ປິດເບຣກເກີຖ້າໄດ້ກິ່ນໄໝ້ ຫຼື ເຫັນນ້ຳຢອດໃກ້ປັກສຽບໄຟ."),
    ("electrical-ac", ["ac ", "ແອເສຍ", "ຄອມເພຣສເຊີ"], "ແອຄອມເພຣສເຊີ / ລະບົບຄວາມເຢັນມີບັນຫາ",
     "ກວດແຜ່ນກອງອາກາດວ່າຕັນບໍ; ຊ່າງແອໃກ້ຄຽງຮັບເຕີມນ້ຳຢາ ແລະ ປ່ຽນແຄັບປາຊິເຕີ."),
    ("electrical-ac", ["electric", "ໄຟຟ້າດັບ", "ໄຟດັບ", "ໄຟຟ້າຊັອດ"], "ໄຟຟ້າດັບ / ປັກສຽບມີປະກາຍໄຟ",
     "ປິດເບຣກເກີວົງຈອນທີ່ມີບັນຫາທັນທີ ແລະ ຢ່າແຕະຕູ້ໄຟທີ່ປຽກນ້ຳ."),
    # ຄລີນິກ ແລະ ຮ້ານຂາຍຢາ
    ("clinic-pharmacy", ["medicine", "ຮ້ານຂາຍຢາ", "ຊື້ຢາ", "ຕ້ອງການຢາ"], "ຕ້ອງການຮ້ານຂາຍຢາ / ຢາປິ່ນປົວ",
     "ຖ້າເຈັບໜ້າເອິກຮຸນແຮງ, ຫາຍໃຈຍາກ ຫຼື ບາດເຈັບຮ້າຍແຮງ ໃຫ້ໂທຫາລົດພະຍາບານສຸກເສີນທັນທີ."),
    ("clinic-pharmacy", ["fever", "ເປັນໄຂ້", "ໄຂ້", "ປະຖົມພະຍາບານ"], "ເປັນໄຂ້ / ເຈັບປ່ວຍເລັກນ້ອຍ / ປະຖົມພະຍາບານ",
     "ດື່ມນ້ຳໃຫ້ພຽງພໍ ແລະ ປຶກສາເພສັດຊະກອນ ຫຼື ຄລີນິກໃກ້ຄຽງ."),
]


DEMO_SHOP_TEMPLATES = [
    {
        "cat_slug": "car-auto-repair",
        "name": "ສະປີດຟິກ ອູ່ສ້ອມລົດ ແລະ ກວດວິເຄາະ",
        "description": "ອູ່ສ້ອມລົດຄົບວົງຈອນ ຊ່ຽວຊານບັນຫາລົດສະຕາດບໍ່ຕິດ, ເຄື່ອງຈັກມີສຽງດັງ, ໝໍ້ນ້ຳຮ້ອນ, ສ້ອມເບກ ແລະ ກວດເຄື່ອງດ້ວຍເຄື່ອງສະແກນ OBD.",
        "problem_tags": "ລົດສະຕາດບໍ່ຕິດ, ເຄື່ອງຈັກມີສຽງດັງ, ມີຄວັນ ເຄື່ອງຮ້ອນ, ເບກມີສຽງດັງ, ນ້ຳມັນຮົ່ວ, ໄຟເຕືອນເຄື່ອງຈັກ",
        "phone": "+856 20 5560 1234",
        "street": "ຖະໜົນລ້ານຊ້າງ",
        "d_lat": 0.0085,
        "d_lng": 0.0062,
        "opening_hours": "08:00 - 20:00",
        "is_emergency_24h": False,
        "status": "APPROVED",
    },
    {
        "cat_slug": "towing-roadside",
        "name": "ຣາປິດຣີສຄິວ ລົດລາກ ແລະ ຊ່ວຍເຫຼືອສຸກເສີນ 24 ຊົ່ວໂມງ",
        "description": "ບໍລິການກູ້ໄພກາງທາງ, ລາກລົດດ້ວຍລົດບັນທຸກພື້ນຮາບ, ຊ່ວຍເຫຼືອລົດເສຍເທິງທາງຫຼວງ, ກະຕຸ້ນແບັດ ແລະ ສົ່ງນ້ຳມັນສຸກເສີນ ທັງກາງເວັນ ແລະ ກາງຄືນ.",
        "problem_tags": "ລົດຕິດກາງທາງ, ລົດລາກສຸກເສີນ, ລົດສະຕາດບໍ່ຕິດ, ລົດເສຍກາງທາງ, ກູ້ໄພອຸບັດເຫດ, ກະຕຸ້ນແບັດ",
        "phone": "+856 20 9999 2407",
        "street": "ຖະໜົນໄກສອນ ພົມວິຫານ",
        "d_lat": -0.0110,
        "d_lng": 0.0095,
        "opening_hours": "24 ຊົ່ວໂມງ (ທຸກວັນ)",
        "is_emergency_24h": True,
        "status": "APPROVED",
    },
    {
        "cat_slug": "tire-battery",
        "name": "ໂປຣໄທຣ໌ ຢາງລົດ ແລະ ແບັດເຕີຣີ້ເຄື່ອນທີ່",
        "description": "ປະຢາງແບນທັງຢູ່ຮ້ານ ແລະ ນອກສະຖານທີ່, ຖ່ວງລໍ້, ຂາຍຢາງໃໝ່ ແລະ ປ່ຽນແບັດເຕີຣີ້ລົດພາຍໃນ 30 ນາທີ.",
        "problem_tags": "ຢາງລົດແບນ, ຢາງຮົ່ວ, ແບັດເຕີຣີ້ລົດໝົດ, ກະຕຸ້ນແບັດ, ລໍ້ສັ່ນ, ລົດສະຕາດບໍ່ຕິດ",
        "phone": "+856 20 5558 811",
        "street": "ຖະໜົນເຊເສດຖາ",
        "d_lat": 0.0042,
        "d_lng": -0.0078,
        "opening_hours": "07:00 - 22:00",
        "is_emergency_24h": True,
        "status": "APPROVED",
    },
    {
        "cat_slug": "motorcycle-repair",
        "name": "ມໍເຕີດັອກເຕີ ອູ່ສ້ອມລົດຈັກ",
        "description": "ສ້ອມແປງລົດຈັກ ແລະ ສະກູດເຕີຢ່າງໄວ: ສາຍແອວຂາດ, ຢາງແບນ, ຫົວທຽນ, ກາບູເຣເຕີ ແລະ ເບກ.",
        "problem_tags": "ລົດຈັກສະຕາດບໍ່ຕິດ, ລົດຈັກຢາງແບນ, ໂສ້ລົດຈັກຂາດ, ສ້ອມເບກລົດຈັກ",
        "phone": "+856 20 5532 1774",
        "street": "ຖະໜົນທ່າເດື່ອ",
        "d_lat": -0.0068,
        "d_lng": -0.0104,
        "opening_hours": "08:30 - 19:30",
        "is_emergency_24h": False,
        "status": "APPROVED",
    },
    {
        "cat_slug": "phone-computer",
        "name": "ໄອເທັກ ເອັກສະເພຣສ ຄລີນິກໂທລະສັບ ແລະ ແລັບທັອບ",
        "description": "ປ່ຽນໜ້າຈໍໂທລະສັບແຕກພາຍໃນ 1 ຊົ່ວໂມງ, ທຳຄວາມສະອາດເມນບອດຕົກນ້ຳ, ປ່ຽນແບັດເຕີຣີ້ ແລະ ກູ້ແລັບທັອບທີ່ເປີດບໍ່ຕິດ.",
        "problem_tags": "ໜ້າຈໍໂທລະສັບແຕກ, ໂທລະສັບຕົກນ້ຳ, ແລັບທັອບເປີດບໍ່ຕິດ, ແບັດໂທລະສັບໝົດໄວ",
        "phone": "+856 20 7701 122",
        "street": "ສູນການຄ້າ ຊັ້ນ 1 ຫ້ອງ 104",
        "d_lat": 0.0145,
        "d_lng": -0.0040,
        "opening_hours": "10:00 - 21:00",
        "is_emergency_24h": False,
        "status": "APPROVED",
    },
    {
        "cat_slug": "home-plumbing",
        "name": "ອາກວາເຊຟ ຊ່າງປະປາສຸກເສີນ",
        "description": "ຮັບມືໄວສຳລັບທໍ່ນ້ຳແຕກ, ຫ້ອງນ້ຳຮົ່ວ, ທໍ່ລະບາຍນ້ຳຕັນ, ນ້ຳອ່ອນ ແລະ ສ້ອມປັ໊ມນ້ຳ.",
        "problem_tags": "ທໍ່ນ້ຳຮົ່ວ, ທໍ່ນ້ຳແຕກນ້ຳຖ້ວມ, ສ້ວມຕັນ, ປັ໊ມນ້ຳເສຍ",
        "phone": "+856 20 5544 3909",
        "street": "ຖະໜົນຫຼວງວຽງຈັນ ໃກ້ແມ່ນ້ຳຂອງ",
        "d_lat": -0.0160,
        "d_lng": 0.0140,
        "opening_hours": "24 ຊົ່ວໂມງ (ສຸກເສີນ)",
        "is_emergency_24h": True,
        "status": "APPROVED",
    },
    {
        "cat_slug": "electrical-ac",
        "name": "ຄູນບຣີສ ຊ່າງແອເຢັນ ແລະ ໄຟຟ້າໃນເຮືອນ",
        "description": "ຊ່າງຊ່ຽວຊານແອເຢັນບໍ່ເຢັນ, ນ້ຳຮົ່ວຈາກແອ, ສ້ອມຄອມເພຣສເຊີ, ເບຣກເກີຕັດ ແລະ ກວດສາຍໄຟ.",
        "problem_tags": "ແອເຢັນບໍ່ເຢັນ, ແອນ້ຳຮົ່ວ, ໄຟຟ້າດັບເບຣກເກີຕັດ, ປັກສຽບມີໄຟຟ້າຊັອດ",
        "phone": "+856 20 5560 334",
        "street": "ບ້ານໜອງບອນ",
        "d_lat": 0.0190,
        "d_lng": 0.0155,
        "opening_hours": "08:00 - 19:00",
        "is_emergency_24h": False,
        "status": "APPROVED",
    },
    # ຮ້ານລໍຖ້າການອະນຸມັດ — ໃຫ້ຜູ້ດູແລລະບົບກົດອະນຸມັດ
    {
        "cat_slug": "car-auto-repair",
        "name": "ຊັນໄຣສ໌ ອູ່ລົດໄຮບຣິດ ແລະ ລົດໄຟຟ້າ",
        "description": "ອູ່ຊ່ຽວຊານລົດໄຮບຣິດ ແລະ ລົດໄຟຟ້າ, ໄຟເຕືອນໜ້າປັດ, ລະບົບລະບາຍຄວາມຮ້ອນ, ຊ່ວງລ່າງ ແລະ ແອລົດ.",
        "problem_tags": "ໄຟເຕືອນໄຮບຣິດ, ກວດແບັດລົດໄຟຟ້າ, ລົດສະຕາດບໍ່ຕິດ, ແອລົດບໍ່ເຢັນ, ເບກມີສຽງ",
        "phone": "+856 20 8811 2399",
        "street": "ຖະໜົນວົງວຽນຕາເວັນອອກ ເລກ 77",
        "d_lat": 0.0115,
        "d_lng": -0.0125,
        "opening_hours": "08:30 - 18:30",
        "is_emergency_24h": False,
        "status": "PENDING",
    },
    {
        "cat_slug": "clinic-pharmacy",
        "name": "ແຄຣ໌ພລັສ ຮ້ານຂາຍຢາກາງຄືນ ແລະ ປະຖົມພະຍາບານ",
        "description": "ເພສັດຊະກອນໃຫ້ຄຳປຶກສາຕອນກາງຄືນ ມີຢາແກ້ໄຂ້ ແກ້ປວດ, ຜ້າພັນບາດແຜ, ຢາແກ້ແພ້ ແລະ ວັດແທກຄວາມດັນ.",
        "problem_tags": "ຢາແກ້ໄຂ້, ຮ້ານຂາຍຢາເປີດດຶກ, ປະຖົມພະຍາບານ, ປວດທ້ອງ ແພ້",
        "phone": "+856 20 8720 2454",
        "street": "ອາຄານ B ຕະຫຼາດເຊົ້າ",
        "d_lat": -0.0052,
        "d_lng": 0.0048,
        "opening_hours": "08:00 - 23:30",
        "is_emergency_24h": False,
        "status": "PENDING",
    },
]


def seed_shops_around_coordinates(
    db: Session,
    center_lat: float,
    center_lng: float,
    area_name: str,
    owner: User,
    admin: User | None = None,
) -> int:
    """Spawn realistic demo shops around given coordinates (skips ones that already exist)."""
    cat_by_slug = {c.slug: c for c in db.query(Category).all()}
    created_count = 0

    for tpl in DEMO_SHOP_TEMPLATES:
        cat = cat_by_slug.get(tpl["cat_slug"])
        if not cat:
            continue
        target_lat = round(center_lat + tpl["d_lat"], 6)
        target_lng = round(center_lng + tpl["d_lng"], 6)
        shop_name = (
            tpl["name"]
            if area_name == DEFAULT_AREA_NAME
            else f"{tpl['name']} ({area_name})"
        )

        exists = db.query(Shop).filter(Shop.name == shop_name).first()
        if exists:
            continue

        shop = Shop(
            owner_id=owner.id,
            category_id=cat.id,
            name=shop_name,
            description=tpl["description"],
            problem_tags=tpl["problem_tags"],
            phone=tpl["phone"],
            address=f"{tpl['street']}, {area_name}",
            latitude=target_lat,
            longitude=target_lng,
            opening_hours=tpl["opening_hours"],
            is_emergency_24h=tpl["is_emergency_24h"],
            status=tpl["status"],
        )
        db.add(shop)
        created_count += 1

        if tpl["status"] == "PENDING" and admin is not None:
            db.add(
                Notification(
                    user_id=admin.id,
                    title=f"ຮ້ານລໍຖ້າການກວດສອບ: {shop_name}",
                    message=(
                        f"{owner.full_name} ໄດ້ສົ່ງຮ້ານ '{shop_name}' ທີ່ {tpl['street']}, {area_name}. "
                        "ກົດເພື່ອກວດເບິ່ງຈຸດແຜນທີ່ ແລະ ອະນຸມັດ."
                    ),
                    notif_type="SHOP_PENDING",
                    link_url="/admin/approvals",
                )
            )

    db.commit()
    return created_count


def seed_initial_data(db: Session) -> None:
    """Idempotently populate demo accounts, categories, problem keywords, and initial shops."""
    admin = db.query(User).filter(User.email == "admin@searchwant.com").first()
    if not admin:
        admin = User(
            email="admin@searchwant.com",
            password_hash=hash_password("admin123"),
            full_name="ຜູ້ດູແລລະບົບ",
            phone="+856 20 5500 0001",
            role="ADMIN",
        )
        db.add(admin)

    owner = db.query(User).filter(User.email == "owner@searchwant.com").first()
    if not owner:
        owner = User(
            email="owner@searchwant.com",
            password_hash=hash_password("owner123"),
            full_name="ສົມໃຈ ເຈົ້າຂອງອູ່ລົດ",
            phone="+856 20 5560 1230",
            role="SHOP_OWNER",
        )
        db.add(owner)

    customer = db.query(User).filter(User.email == "user@searchwant.com").first()
    if not customer:
        customer = User(
            email="user@searchwant.com",
            password_hash=hash_password("user123"),
            full_name="ບຸນມີ ຄົນຂັບລົດ",
            phone="+856 20 5911 2233",
            role="USER",
        )
        db.add(customer)

    db.commit()
    db.refresh(admin)
    db.refresh(owner)

    # Seed Categories
    existing_cats = {c.slug: c for c in db.query(Category).all()}
    for c_data in CATEGORIES_DATA:
        if c_data["slug"] not in existing_cats:
            db.add(Category(**c_data))
    db.commit()

    cat_map = {c.slug: c for c in db.query(Category).all()}

    # Seed Problem Keywords (Lao + English synonyms share one symptom label/advice)
    if db.query(ProblemKeyword).count() == 0:
        for slug, keywords, label, hint in KEYWORDS_DATA:
            cat = cat_map.get(slug)
            if not cat:
                continue
            for kw in keywords:
                db.add(
                    ProblemKeyword(
                        category_id=cat.id,
                        keyword=kw,
                        symptom_label=label,
                        advice_hint=hint,
                    )
                )
        db.commit()

    # Seed Initial Shops if database has none
    if db.query(Shop).count() == 0:
        seed_shops_around_coordinates(
            db=db,
            center_lat=DEFAULT_CENTER_LAT,
            center_lng=DEFAULT_CENTER_LNG,
            area_name=DEFAULT_AREA_NAME,
            owner=owner,
            admin=admin,
        )
