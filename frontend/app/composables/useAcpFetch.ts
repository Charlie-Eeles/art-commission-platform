import { useLogto } from "@logto/vue";

export enum HTTPMethods {
  GET = "GET",
  POST = "POST",
  PUT = "PUT",
  DELETE = "DELETE",
  PATCH = "PATCH",
}

export function useAcpFetch() {
  const { isAuthenticated, getAccessToken } = useLogto();

  const {
    public: { apiBaseUrl, logtoApiResource },
  } = useRuntimeConfig();

  return async function acpFetch(
    url: string,
    method: HTTPMethods = HTTPMethods.GET,
    body: Record<string, unknown> = {},
  ) {
    if (!isAuthenticated.value) return;

    const accessToken = await getAccessToken(logtoApiResource);

    if (!accessToken) return;

    return $fetch(`${apiBaseUrl}${url}`, {
      method,
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      ...(method === HTTPMethods.GET ? {} : { body }),
    });
  };
}
