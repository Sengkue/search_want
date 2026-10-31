const STATUS_LABELS: Record<string, string> = {
  PENDING: 'ລໍຖ້າການອະນຸມັດ',
  APPROVED: 'ອະນຸມັດແລ້ວ',
  REJECTED: 'ຖືກປະຕິເສດ',
  SUSPENDED: 'ຢຸດຊົ່ວຄາວ',
}

const ROLE_LABELS: Record<string, string> = {
  USER: 'ຜູ້ໃຊ້ທົ່ວໄປ',
  SHOP_OWNER: 'ເຈົ້າຂອງຮ້ານ',
  ADMIN: 'ຜູ້ດູແລລະບົບ',
}

const LOG_ACTION_LABELS: Record<string, string> = {
  APPROVED: 'ອະນຸມັດ',
  REJECTED: 'ປະຕິເສດ',
  SUSPENDED: 'ຢຸດຊົ່ວຄາວ',
  RESUBMITTED: 'ສົ່ງຄືນໃໝ່',
}

/** Lao display labels for backend enum values + Lao date formatting. */
export function useLabels() {
  const statusLabel = (s: string) => STATUS_LABELS[s] ?? s
  const roleLabel = (r: string) => ROLE_LABELS[r] ?? r
  const logActionLabel = (a: string) => LOG_ACTION_LABELS[a] ?? a
  const formatDateTime = (iso: string) => new Date(iso).toLocaleString('lo-LA')

  return { statusLabel, roleLabel, logActionLabel, formatDateTime }
}

