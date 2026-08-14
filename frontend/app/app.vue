<template>
  <div>
    <NuxtRouteAnnouncer />

    <UApp v-if="isAuthenticated || isCallbackRoute">
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </UApp>

    <div
      v-else
      class="flex min-h-screen flex-col items-center justify-center gap-4 text-center"
    >
      <p>You must be signed in to access the Art Commission Platform</p>

      <Button type="button" label="Sign in" @click="startSignIn">
        <template #icon>
          <Icon name="material-symbols:login" class="size-4" />
        </template>
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLogto } from "@logto/vue";

const route = useRoute();
const { signIn, isAuthenticated } = useLogto();
const callBackRoute = "/auth/callback";

const isCallbackRoute = computed(() => route.path === callBackRoute);

function startSignIn() {
  signIn(`${window.location.origin}${callBackRoute}`);
}
</script>
