<template>
  <span
    class="sw-app-icon-badge"
    :style="{
      width: `${size}px`,
      height: `${size}px`,
      borderRadius: `${Math.round(size * 0.24)}px`,
    }"
  >
    <img
      src="/app-icon-96.webp"
      alt="Search-Want"
      :width="size"
      :height="size"
      decoding="async"
      style="display: block; width: 100%; height: 100%; object-fit: cover"
    />
  </span>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    size?: number
  }>(),
  {
    size: 36,
  },
)
</script>
