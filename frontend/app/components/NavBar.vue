<template>
  <header class="bg-white shadow-md mb-4 h-16">
    <div class="container mx-auto h-full flex items-center">
      <Menubar class="w-full !border-0 !rounded-none z-[60]" :model="menuItems">
        <template #start>
          <NuxtLink to="/" class="flex items-center mr-4">
            Art Commission Platform
          </NuxtLink>
        </template>

        <template #item="{ item, props, hasSubmenu }">
          <NuxtLink
            v-if="item.to"
            v-bind="props.action"
            class="inline-flex h-full items-center gap-2 text-sm font-normal"
            :to="item.to"
          >
            <Icon v-if="item.icon" :name="item.icon" class="size-4 shrink-0" />

            <span class="text-inherit leading-inherit">{{ item.label }}</span>

            <Icon
              v-if="hasSubmenu"
              name="heroicons:chevron-down"
              class="ml-1 size-4 shrink-0"
            />
          </NuxtLink>

          <button
            v-else
            type="button"
            v-bind="props.action"
            class="inline-flex h-full items-center gap-2 text-sm font-normal"
          >
            <Icon v-if="item.icon" :name="item.icon" class="size-4 shrink-0" />

            <span class="flex flex-col">
              <span class="text-inherit leading-inherit">{{ item.label }}</span>
            </span>

            <Icon
              v-if="hasSubmenu"
              name="heroicons:chevron-down"
              class="ml-1 size-4 shrink-0"
            />
          </button>
        </template>
      </Menubar>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useLogto } from "@logto/vue";

const { signIn, signOut, isAuthenticated } = useLogto();

const menuItems = computed<MenuItem[]>(() => {
  return [
    {
      label: "Explore",
      to: "/explore",
      icon: "material-symbols:explore-outline",
    },

    ...(isAuthenticated.value
      ? [
          {
            label: "Your portfolio",
            to: "/portfolio/your-portfolio",
            icon: "material-symbols:palette-outline",
          },
        ]
      : []),

    {
      label: "Account",
      icon: "material-symbols:account-circle-outline",
      items: [
        isAuthenticated.value
          ? {
              label: "Sign out",
              icon: "material-symbols:logout",
              command: () => {
                signOut(window.location.origin);
              },
            }
          : {
              label: "Sign in",
              icon: "material-symbols:login",
              command: () => {
                signIn(`${window.location.origin}/auth/callback`);
              },
            },
      ],
    },
  ];
});
</script>

<style>
.p-menubar-root-list {
  margin-left: auto;
}

.p-menubar {
  background: transparent;
}

.p-menubar .p-menuitem-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 0.375rem 0.5rem;
}

.p-menubar .p-menubar-button {
  margin-left: auto;
}

.p-menubar .p-submenu-list .p-menuitem-link {
  justify-content: flex-start;
  height: auto;
  padding: 0.625rem 0.75rem;
}
</style>
