<template>
  <div :class="['playx-logo-container', variant]">
    <svg
      class="logo-svg"
      viewBox="0 0 200 50"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <!-- Geometric Cutter Node Icon -->
      <g class="logo-icon-group">
        <rect x="2" y="6" width="38" height="38" rx="10" fill="url(#logoGrad)" />
        <path d="M12 16L28 16L32 32L16 32Z" fill="#FFFFFF" fill-opacity="0.9" />
        <path d="M16 22H26M18 26H24" stroke="#0071E3" stroke-width="2" stroke-linecap="round"/>
        <circle cx="30" cy="16" r="3" fill="#34C759" />
      </g>
      <!-- Brand Text (only rendered in full variant) -->
      <g v-if="variant === 'full'" class="logo-text-group">
        <text x="50" y="27" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif" font-weight="800" font-size="20" fill="#1D1D1F" letter-spacing="-0.5">PLAYX</text>
        <text x="50" y="40" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif" font-weight="600" font-size="10" fill="#0071E3" letter-spacing="1">WASTE OPTIMISER</text>
      </g>
      <defs>
        <linearGradient id="logoGrad" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop stop-color="#0071E3"/>
          <stop offset="1" stop-color="#0047AB"/>
        </linearGradient>
      </defs>
    </svg>
  </div>
</template>

<script>
export default {
  name: "PlayxLogo",
  props: {
    variant: {
      type: String,
      default: "full" // 'full' or 'compact'
    }
  }
};
</script>

<style scoped>
.playx-logo-container {
  display: inline-flex;
  align-items: center;
}
.logo-svg {
  height: 40px;
  width: auto;
}
.playx-logo-container.compact .logo-svg {
  width: 42px;
}
</style>
