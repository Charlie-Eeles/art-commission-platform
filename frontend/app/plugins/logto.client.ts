import { createLogto, UserScope, type LogtoConfig } from "@logto/vue";

export default defineNuxtPlugin((nuxtApp) => {
  const runtimeConfig = useRuntimeConfig();

  const config: LogtoConfig = {
    endpoint: runtimeConfig.public.logtoEndpoint,
    appId: runtimeConfig.public.logtoAppId,
    resources: [runtimeConfig.public.logtoApiResource],
    scopes: [UserScope.Email],
  };

  nuxtApp.vueApp.use(createLogto, config);
});
