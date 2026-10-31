<template>
  <v-container class="py-4 py-md-6 px-3" style="max-width: 900px">
    <v-card class="sw-hero-card pa-4 pa-md-6 mb-3">
      <div class="d-flex align-center ga-3 mb-3">
        <BrandLogo :size="40" />
        <div>
          <h1 class="text-title-medium text-md-title-large font-weight-black" style="line-height: 1.25">
            ນະໂຍບາຍຄວາມເປັນສ່ວນຕົວ ແລະ ຂໍ້ກຳນົດການໃຊ້ງານ
          </h1>
          <div class="text-body-small text-medium-emphasis">
            Search-Want — ຄົ້ນຫາຮ້ານໃກ້ຄຽງຈາກບັນຫາຂອງທ່ານ (ອັບເດດຫຼ້າສຸດ: 2026)
          </div>
        </div>
      </div>

      <v-divider class="mb-4" />

      <div class="mb-4">
        <h2 class="text-title-small font-weight-bold mb-1 d-flex align-center ga-2">
          <v-icon icon="mdi-crosshairs-gps" size="18" color="primary" />
          <span>1. ຂໍ້ມູນຕຳແໜ່ງ GPS ແລະ ການຄົ້ນຫາຮ້ານໃກ້ຄຽງ</span>
        </h2>
        <p class="text-body-small text-medium-emphasis mb-0">
          Search-Want ໃຊ້ພິກັດ GPS ຈາກອຸປະກອນຂອງທ່ານສະເພາະເມື່ອທ່ານກົດອະນຸຍາດ ເພື່ອຄຳນວນໄລຍະທາງໄປຫາຮ້ານສ້ອມແປງ ແລະ ບໍລິການທີ່ຜ່ານການອະນຸມັດໃກ້ຕົວທ່ານເທົ່ານັ້ນ. ລະບົບບໍ່ໄດ້ນຳຂໍ້ມູນຕຳແໜ່ງສ່ວນຕົວຂອງທ່ານໄປຂາຍຕໍ່ໃຫ້ບຸກຄົນທີສາມ.
        </p>
      </div>

      <div class="mb-4">
        <h2 class="text-title-small font-weight-bold mb-1 d-flex align-center ga-2">
          <v-icon icon="mdi-google" size="18" color="primary" />
          <span>2. ການສະແດງໂຄສະນາ Google AdSense ແລະ Cookies</span>
        </h2>
        <p class="text-body-small text-medium-emphasis mb-2">
          ເວັບໄຊນີ້ໃຊ້ບໍລິການ <strong>Google AdSense</strong> ເພື່ອສະແດງໂຄສະນາທີ່ກ່ຽວຂ້ອງກັບຜູ້ໃຊ້ງານ:
        </p>
        <ul class="text-body-small text-medium-emphasis pl-5 mb-0">
          <li class="mb-1">
            ຜູ້ໃຫ້ບໍລິການບຸກຄົນທີສາມ ລວມເຖິງ <strong>Google</strong> ໃຊ້ຄຸກກີ້ (Cookies) ເພື່ອສະແດງໂຄສະນາໂດຍອີງຕາມການເຂົ້າຊົມເວັບໄຊນີ້ ຫຼື ເວັບໄຊອື່ນໆ ໃນອິນເຕີເນັດຂອງຜູ້ໃຊ້.
          </li>
          <li class="mb-1">
            ການໃຊ້ຄຸກກີ້ໂຄສະນາຂອງ Google ຊ່ວຍໃຫ້ Google ແລະ ພາດເນີສາມາດສະແດງໂຄສະນາທີ່ເໝາະສົມກັບຄວາມສົນໃຈຂອງທ່ານ.
          </li>
          <li>
            ທ່ານສາມາດປິດການໃຊ້ໂຄສະນາແບບປັບແຕ່ງສະເພາະບຸກຄົນ (Personalized Advertising) ໄດ້ທຸກເວລາ ທີ່ໜ້າ
            <a href="https://adssettings.google.com" target="_blank" rel="noopener" class="text-primary font-weight-bold">
              ການຕັ້ງຄ່າໂຄສະນາຂອງ Google (Google Ads Settings)
            </a>
            ແລະ ສຶກສາເພີ່ມເຕີມໄດ້ທີ່
            <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener" class="text-primary font-weight-bold">
              ນະໂຍບາຍໂຄສະນາຂອງ Google
            </a>.
          </li>
        </ul>
      </div>

      <div class="mb-4">
        <h2 class="text-title-small font-weight-bold mb-1 d-flex align-center ga-2">
          <v-icon icon="mdi-shield-check-outline" size="18" color="success" />
          <span>3. ຂໍ້ມູນຮ້ານຄ້າ ແລະ ການກວດສອບໂດຍຜູ້ດູແລລະບົບ</span>
        </h2>
        <p class="text-body-small text-medium-emphasis mb-0">
          ເຈົ້າຂອງຮ້ານທີ່ລົງທະບຽນເພີ່ມຮ້ານເທິງແຜນທີ່ ຍິນຍອມໃຫ້ສະແດງຊື່ຮ້ານ, ປະເພດບໍລິການ, ເບີໂທຕິດຕໍ່, ເວລາເປີດ-ປິດ ແລະ ພິກັດແຜນທີ່ຕໍ່ສາທາລະນະ ຫຼັງຈາກຜູ້ດູແລລະບົບກວດສອບ ແລະ ອະນຸມັດແລ້ວ.
        </p>
      </div>

      <div class="d-flex flex-wrap align-center justify-space-between ga-2 pt-3 border-t">
        <span class="text-body-small text-medium-emphasis">
          ຕິດຕໍ່ຜູ້ດູແລລະບົບ: <code>admin@searchwant.com</code>
        </span>
        <v-btn to="/" color="primary" variant="tonal" size="small" prepend-icon="mdi-arrow-left">
          ກັບໄປໜ້າຄົ້ນຫາຮ້ານໃກ້ຄຽງ
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

