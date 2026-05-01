<template>
  <UHeader>
    <template #left>
      <NuxtLink to="/" class="font-semibold">
        Art Commission Platform
      </NuxtLink>
    </template>

    <template #right>
      <UNavigationMenu :items="items" class="hidden md:flex" />
    </template>

    <template #body>
      <UNavigationMenu
        :items="items"
        orientation="vertical"
        class="md:hidden"
      />
    </template>
  </UHeader>
</template>

<script setup lang="ts">
const items = [
  {
    label: "Explore",
    to: "/explore", //TODO: Add explore page
  },
  {
    label: "Your portfolio",
    to: "/portfolio/1", //TODO: Make this dynamic
  },
  {
    label: "Account",
    to: "/account", //TODO: Add account management (probably not a page but a drop-down)
  },
];
</script>
