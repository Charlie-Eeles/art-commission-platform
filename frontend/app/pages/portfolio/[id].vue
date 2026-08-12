<template>
  <div class="mx-auto max-w-5xl">
    <template v-if="portfolio?.userId">
      <div class="mb-6">
        <NuxtLink to="/explore">
          <Button label="Back to explore" severity="secondary" variant="text">
            <template #icon>
              <Icon name="material-symbols:arrow-back" class="size-4" />
            </template>
          </Button>
        </NuxtLink>
      </div>

      <Card>
        <template #title>
          {{ portfolio.description || "Untitled portfolio" }}
        </template>

        <template #subtitle>
          {{ portfolio.commissionSlots }} commission slots available
        </template>

        <template #content>
          <PortfolioCarousel
            v-if="portfolioImages.length"
            :images="portfolioImages.map(toCarouselImage)"
          />

          <div v-else class="flex flex-col items-center py-12 text-center">
            <Icon
              name="material-symbols:imagesmode-outline"
              class="mb-3 size-10 text-gray-400"
            />

            <p class="text-gray-500">This portfolio has no images.</p>
          </div>
        </template>

        <template #footer>
          <div class="flex flex-col items-start gap-3">
            <Button
              label="Request commission"
              :loading="isSubmitting"
              :disabled="isSubmitted"
              @click="submitRequest"
            >
              <template #icon>
                <Icon name="material-symbols:send-outline" class="size-4" />
              </template>
            </Button>

            <p v-if="isSubmitted" class="text-sm text-green-600">
              Your commission request has been submitted.
            </p>

            <p v-else-if="requestError" class="text-sm text-red-600">
              {{ requestError }}
            </p>
          </div>
        </template>
      </Card>
    </template>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const acpFetch = useAcpFetch();

const isSubmitting = ref(false);
const isSubmitted = ref(false);
const requestError = ref<string | null>(null);

const portfolio = (await acpFetch(
  `/explore/portfolios/${route.params.id}`,
)) as PublicPortfolio;

const portfolioImages = computed(() =>
  Array.isArray(portfolio?.images) ? portfolio.images : [],
);

async function submitRequest() {
  isSubmitting.value = true;
  requestError.value = null;

  try {
    await acpFetch(
      `/explore/portfolios/${route.params.id}/requests`,
      HTTPMethods.POST,
    );

    isSubmitted.value = true;
  } catch (error: unknown) {
    const fetchError = error as {
      data?: {
        detail?: string;
      };
    };

    requestError.value =
      fetchError.data?.detail ?? "Unable to submit the commission request.";
  } finally {
    isSubmitting.value = false;
  }
}
</script>
