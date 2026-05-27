import { createLogto, type LogtoConfig } from "@logto/vue";

export default defineNuxtPlugin((nuxtApp) => {
  const runtimeConfig = useRuntimeConfig();

  const config: LogtoConfig = {
    endpoint: runtimeConfig.public.logtoEndpoint,
    appId: runtimeConfig.public.logtoAppId,
  };

  nuxtApp.vueApp.use(createLogto, config);
});
