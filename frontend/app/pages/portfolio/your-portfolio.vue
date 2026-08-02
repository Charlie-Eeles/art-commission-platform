<template>
  <div>
    <header class="py-2">
      <h1 class="text-3xl font-semibold">Your Portfolio</h1>
      <p class="mt-2 text-gray-500">Upload and manage your artwork.</p>
    </header>

    <Card class="mb-8">
      <template #title>Portfolio settings</template>

      <template #content>
        <form class="flex flex-col gap-4" @submit.prevent="saveSettings">
          <div class="flex flex-col gap-2">
            <label for="portfolio-description" class="text-sm font-medium">
              Description
            </label>
            <Textarea
              id="portfolio-description"
              v-model="settings.description"
              rows="4"
              auto-resize
              placeholder="Tell visitors about your work"
              :disabled="settingsLoading"
              fluid
            />
          </div>

          <div class="flex flex-col gap-2">
            <label for="commission-slots" class="text-sm font-medium">
              Commission slots
            </label>
            <InputNumber
              v-model="settings.commissionSlots"
              input-id="commission-slots"
              :min="0"
              :disabled="settingsLoading"
              fluid
            />
          </div>

          <div class="flex items-center justify-between gap-4">
            <div>
              <label for="portfolio-public" class="font-medium">
                Publish portfolio
              </label>
              <p class="text-sm text-gray-500">
                Make your portfolio visible to other users.
              </p>
            </div>

            <ToggleSwitch
              v-model="settings.isPublic"
              input-id="portfolio-public"
              :disabled="settingsLoading"
            />
          </div>

          <div>
            <Button
              type="submit"
              :label="
                settings.isPublic ? 'Save and publish' : 'Save as private'
              "
              :loading="settingsSaving"
              :disabled="settingsLoading"
            >
              <template #icon>
                <Icon name="material-symbols:save-outline" class="size-4" />
              </template>
            </Button>
          </div>
        </form>
      </template>
    </Card>

    <Card class="mb-8">
      <template #title>Add artwork</template>

      <template #content>
        <form
          class="grid gap-4 md:grid-cols-[1fr_1fr_auto] md:items-end"
          @submit.prevent="uploadImage"
        >
          <div class="flex flex-col gap-2">
            <label for="artwork-name" class="text-sm font-medium">
              Artwork name
            </label>
            <InputText
              id="artwork-name"
              v-model="newArtName"
              placeholder="Enter a name"
              :disabled="images.length >= MAX_UPLOADS"
              fluid
            />
          </div>

          <div class="flex flex-col gap-2">
            <label for="artwork-file" class="text-sm font-medium">
              Image
            </label>
            <input
              id="artwork-file"
              ref="fileInput"
              type="file"
              accept="image/*"
              :disabled="images.length >= MAX_UPLOADS"
              class="rounded-md border border-gray-300 px-3 py-2 text-sm file:mr-3 file:border-0 file:bg-transparent file:font-medium disabled:cursor-not-allowed disabled:opacity-50"
              @change="handleFileChange"
            />
          </div>

          <Button
            type="submit"
            label="Upload"
            :disabled="
              images.length >= MAX_UPLOADS ||
              !newArtName.trim() ||
              !selectedFile
            "
          >
            <template #icon>
              <Icon name="material-symbols:upload" class="size-4" />
            </template>
          </Button>

          <p
            v-if="images.length >= MAX_UPLOADS"
            class="text-sm text-gray-500 md:col-span-3"
          >
            You can upload a maximum of {{ MAX_UPLOADS }} artworks.
          </p>
        </form>
      </template>
    </Card>

    <div v-if="images.length" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Card
        v-for="image in images"
        :key="image.id"
        class="overflow-hidden"
        :pt="{ body: { class: 'p-0' }, content: { class: 'p-0' } }"
      >
        <template #header>
          <img
            :src="image.imageUrl"
            :alt="image.artName"
            class="aspect-square w-full object-cover"
          />
        </template>

        <template #content>
          <div class="p-4">
            <div v-if="editingId === image.id" class="flex gap-2">
              <InputText
                v-model="editArtName"
                class="min-w-0 flex-1"
                aria-label="Artwork name"
                autofocus
                @keyup.enter="updateImage(image)"
                @keyup.esc="editingId = undefined"
              />

              <Button
                size="small"
                :disabled="!editArtName.trim()"
                aria-label="Save"
                @click="updateImage(image)"
              >
                <Icon name="material-symbols:save-outline" class="size-4" />
              </Button>

              <Button
                severity="secondary"
                variant="outlined"
                size="small"
                aria-label="Cancel"
                @click="editingId = undefined"
              >
                <Icon name="material-symbols:close" class="size-4" />
              </Button>
            </div>

            <div v-else class="flex items-center justify-between gap-4">
              <h2 class="min-w-0 truncate font-medium">
                {{ image.artName }}
              </h2>

              <div class="flex shrink-0 gap-2">
                <Button
                  severity="secondary"
                  variant="text"
                  rounded
                  size="small"
                  aria-label="Rename image"
                  @click="
                    editingId = image.id;
                    editArtName = image.artName;
                  "
                >
                  <Icon name="material-symbols:edit-outline" class="size-4" />
                </Button>

                <Button
                  severity="danger"
                  variant="text"
                  rounded
                  size="small"
                  aria-label="Delete image"
                  @click="deleteImage(image)"
                >
                  <Icon name="material-symbols:delete-outline" class="size-4" />
                </Button>
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <Card v-else>
      <template #content>
        <div class="flex flex-col items-center py-12 text-center">
          <Icon
            name="material-symbols:image-outline"
            class="mb-3 size-10 text-gray-400"
          />
          <h2 class="font-medium">No portfolio images yet</h2>
          <p class="mt-1 text-sm text-gray-500">
            Upload your first artwork using the form above.
          </p>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useLogto } from "@logto/vue";

type PortfolioImage = {
  id: string;
  artName: string;
  imageUrl: string;
};

type PortfolioSettings = {
  id: string;
  userId: string;
  description: string;
  isPublic: boolean;
  commissionSlots: number;
  createdAt: string;
  updatedAt: string;
};

const MAX_UPLOADS = 6;
const acpFetch = useAcpFetch();
const { isAuthenticated } = useLogto();

const images = ref<PortfolioImage[]>([]);
const settings = reactive({
  description: "",
  isPublic: false,
  commissionSlots: 3,
});
const settingsLoading = ref(true);
const settingsSaving = ref(false);
const newArtName = ref("");
const selectedFile = ref<File>();
const fileInput = ref<HTMLInputElement | null>(null);
const editingId = ref<string>();
const editArtName = ref("");

onMounted(async () => {
  if (!isAuthenticated.value) {
    await navigateTo("/");
    return;
  }

  try {
    const [portfolioImages, portfolioSettings] = await Promise.all([
      acpFetch("/portfolio/images") as Promise<PortfolioImage[]>,
      acpFetch("/portfolio/settings") as Promise<PortfolioSettings>,
    ]);

    images.value = portfolioImages ?? [];
    settings.description = portfolioSettings.description;
    settings.isPublic = portfolioSettings.isPublic;
    settings.commissionSlots = portfolioSettings.commissionSlots;
  } finally {
    settingsLoading.value = false;
  }
});

async function saveSettings() {
  settingsSaving.value = true;

  try {
    const updated = (await acpFetch("/portfolio/settings", HTTPMethods.PUT, {
      description: settings.description,
      isPublic: settings.isPublic,
      commissionSlots: settings.commissionSlots,
    })) as PortfolioSettings;

    settings.description = updated.description;
    settings.isPublic = updated.isPublic;
    settings.commissionSlots = updated.commissionSlots;
  } finally {
    settingsSaving.value = false;
  }
}

function handleFileChange(event: Event) {
  selectedFile.value = (event.target as HTMLInputElement).files?.[0];
}

async function uploadImage() {
  if (
    !selectedFile.value ||
    !newArtName.value.trim() ||
    images.value.length >= MAX_UPLOADS
  ) {
    return;
  }

  const body = new FormData();
  body.append("artName", newArtName.value.trim());
  body.append("image", selectedFile.value);

  const image = (await acpFetch(
    "/portfolio/images",
    HTTPMethods.POST,
    body as unknown as Record<string, unknown>,
  )) as PortfolioImage;

  images.value.unshift(image);
  newArtName.value = "";
  selectedFile.value = undefined;

  if (fileInput.value) {
    fileInput.value.value = "";
  }
}

async function updateImage(image: PortfolioImage) {
  const updated = (await acpFetch(
    `/portfolio/images/${image.id}`,
    HTTPMethods.PATCH,
    { artName: editArtName.value },
  )) as PortfolioImage;

  Object.assign(image, updated);
  editingId.value = undefined;
}

async function deleteImage(image: PortfolioImage) {
  if (!confirm(`Delete "${image.artName}"?`)) return;

  await acpFetch(`/portfolio/images/${image.id}`, HTTPMethods.DELETE);

  images.value = images.value.filter(({ id }) => id !== image.id);
}
</script>
