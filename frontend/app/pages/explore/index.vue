<template>
  <div>
    <div v-if="loading" class="py-12 text-center">Loading portfolios...</div>

    <Card v-else-if="loadError">
      <template #content>
        <div class="py-12 text-center">
          <p class="text-red-500">Failed to load portfolios.</p>

          <Button class="mt-4" label="Try again" @click="loadPortfolios" />
        </div>
      </template>
    </Card>

    <Card v-else-if="!portfolios.length">
      <template #content>
        <div class="flex flex-col items-center py-12 text-center">
          <Icon
            name="material-symbols:imagesmode-outline"
            class="mb-3 size-10 text-gray-400"
          />

          <h2 class="font-medium">No public portfolios found</h2>

          <p class="mt-1 text-sm text-gray-500">
            Published portfolios will appear here.
          </p>
        </div>
      </template>
    </Card>

    <div v-else class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
      <Card v-for="portfolio in portfolios" :key="portfolio.id" class="min-w-0">
        <template #title>
          {{ portfolio.description || "Untitled portfolio" }}
        </template>

        <template #subtitle>
          {{ portfolio.commissionSlots }} commission slots available
        </template>

        <template #content>
          <div class="min-w-0 overflow-hidden">
            <PortfolioCarousel
              v-if="portfolio.images.length"
              :images="portfolio.images.map(toCarouselImage)"
            />

            <p v-else class="py-12 text-center text-gray-500">
              This portfolio has no images.
            </p>
          </div>
        </template>

        <template #footer>
          <NuxtLink :to="`/portfolio/${portfolio.userId}`">
            <Button label="View portfolio">
              <template #icon>
                <Icon name="material-symbols:arrow-forward" class="size-4" />
              </template>
            </Button>
          </NuxtLink>
        </template>
      </Card>
    </div>

    <div
      v-if="totalPages > 1"
      class="mt-8 flex items-center justify-center gap-4"
    >
      <Button
        label="Previous"
        severity="secondary"
        variant="outlined"
        :disabled="page === 1 || loading"
        @click="changePage(page - 1)"
      />

      <span class="text-sm text-gray-500">
        Page {{ page }} of {{ totalPages }}
      </span>

      <Button
        label="Next"
        severity="secondary"
        variant="outlined"
        :disabled="!hasNext || loading"
        @click="changePage(page + 1)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
type PortfolioImage = {
  id: string;
  artName: string;
  imageUrl: string;
  uploadId: string;
  userId: string;
  createdAt: string;
  updatedAt: string;
};

type PublicPortfolio = {
  id: string;
  userId: string;
  description: string;
  commissionSlots: number;
  createdAt: string;
  updatedAt: string;
  images: PortfolioImage[];
};

type PublicPortfolioPage = {
  items: PublicPortfolio[];
  page: number;
  pageSize: number;
  total: number;
  hasNext: boolean;
};

const PAGE_SIZE = 20;
const acpFetch = useAcpFetch();

const portfolios = ref<PublicPortfolio[]>([]);
const page = ref(1);
const total = ref(0);
const hasNext = ref(false);
const loading = ref(true);
const loadError = ref(false);

const totalPages = computed(() => Math.ceil(total.value / PAGE_SIZE));

onMounted(loadPortfolios);

async function loadPortfolios() {
  loading.value = true;
  loadError.value = false;

  try {
    const response = (await acpFetch(
      `/explore/portfolios?page=${page.value}&pageSize=${PAGE_SIZE}`,
    )) as PublicPortfolioPage;

    portfolios.value = response.items ?? [];
    total.value = response.total ?? 0;
    hasNext.value = response.hasNext ?? false;
  } catch {
    loadError.value = true;
  } finally {
    loading.value = false;
  }
}

async function changePage(nextPage: number) {
  page.value = nextPage;
  await loadPortfolios();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function toCarouselImage(image: PortfolioImage) {
  return {
    url: image.imageUrl,
    name: image.artName,
  };
}
</script>
