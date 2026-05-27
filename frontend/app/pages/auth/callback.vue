<template>
  <main class="min-h-screen flex items-center justify-center">
    <p>Signing you in...</p>
  </main>
</template>

<script setup lang="ts">
import { useHandleSignInCallback } from "@logto/vue";

const router = useRouter();

const { isLoading, error } = useHandleSignInCallback(() => {
  router.replace("/");
});

watch(error, (value) => {
  if (value) {
    console.error(value);
  }
});

watch(isLoading, (value) => {
  if (!value && !error.value) {
    router.replace("/");
  }
});
</script>
