import Aura from "@primeuix/themes/aura";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      title: "Art Commission Platform",
    },
  },

  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },

  modules: ["@nuxt/eslint", "@nuxt/ui", "@nuxt/icon", "@primevue/nuxt-module"],

  ssr: false,
  experimental: {
    viteEnvironmentApi: true,
  }, // This fixes an issue with the dev server with SSR false on 4.4.4: https://github.com/nuxt/nuxt/issues/34957

  css: ["~~/assets/css/global.css"],

  components: [
    {
      path: "~/components",
      pathPrefix: false,
    },
  ],

  primevue: {
    options: {
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: ".never-enable-dark",
        },
      },
    },
  },

  colorMode: {
    preference: "light",
  },

  runtimeConfig: {
    public: {
      logtoEndpoint: process.env.NUXT_PUBLIC_LOGTO_ENDPOINT || "",
      logtoAppId: process.env.NUXT_PUBLIC_LOGTO_APP_ID || "",
      logtoApiResource: process.env.NUXT_PUBLIC_LOGTO_API_RESOURCE || "",
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || "",
    },
  },
});
