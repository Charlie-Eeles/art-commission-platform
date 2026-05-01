// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },

  modules: ["@nuxt/eslint", "@nuxt/ui"],

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
});
