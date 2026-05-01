<template>
  <div class="text-blue-500">
    Hello world, welcome to the Art Commission Platform portfolio:
    {{ route.params.id }}!
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
</script>
