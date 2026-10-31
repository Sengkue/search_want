export interface UserOut {
  id: number
  email: string
  full_name: string
  phone: string | null
  role: 'USER' | 'SHOP_OWNER' | 'ADMIN'
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserOut
}

export interface CategoryOut {
  id: number
  name: string
  slug: string
  icon: string
  color: string
  description: string
  shop_count: number
}

export interface ProblemKeywordOut {
  id: number
  category_id: number
  keyword: string
  symptom_label: string
  advice_hint: string
}

export interface ShopPayload {
  category_id: number
  name: string
  description: string
  problem_tags: string
  phone: string
  address: string
  latitude: number
  longitude: number
  opening_hours: string
  is_emergency_24h: boolean
}

export interface ShopOut {
  id: number
  owner_id: number
  owner_name: string
  owner_email?: string | null
  category_id: number
  category_name: string
  category_slug: string
  category_icon: string
  category_color: string
  name: string
  description: string
  problem_tags: string
  phone: string
  address: string
  latitude: number
  longitude: number
  opening_hours: string
  is_emergency_24h: boolean
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'SUSPENDED'
  rejection_reason: string | null
  distance_km: number | null
  match_score: number
  matched_reasons: string[]
  created_at: string
  updated_at: string
}

export interface DiagnosisResult {
  query: string
  matched_categories: CategoryOut[]
  symptom_labels: string[]
  advice_hints: string[]
  notification_summary: string
}

export interface NearbySearchResponse {
  diagnosis: DiagnosisResult
  total_found: number
  radius_km: number | null
  user_lat: number | null
  user_lng: number | null
  shops: ShopOut[]
}

export interface AdminStatsOut {
  pending_count: number
  approved_count: number
  rejected_count: number
  suspended_count: number
  total_users: number
}

export interface ApprovalLogOut {
  id: number
  shop_id: number
  admin_id: number
  admin_name: string
  action: string
  note: string | null
  created_at: string
}

export interface NotificationOut {
  id: number
  title: string
  message: string
  notif_type: string
  link_url: string | null
  is_read: boolean
  created_at: string
}

export interface AdSenseConfig {
  enabled: boolean
  client_id: string
  publisher_id: string
  slot_infeed: string
  slot_banner: string
  auto_ads: boolean
  test_mode: boolean
  ads_txt_line: string
  updated_at: string
}

export interface AdSenseConfigPayload {
  enabled: boolean
  client_id: string
  slot_infeed: string
  slot_banner: string
  auto_ads: boolean
  test_mode: boolean
}


