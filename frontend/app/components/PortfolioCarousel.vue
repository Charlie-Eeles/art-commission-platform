<template>
  <div class="max-w-3xl">
    <UCarousel
      ref="carousel"
      v-slot="{ item }"
      arrows
      :items="images"
      :ui="{ item: 'basis-full' }"
      @select="activeIndex = $event"
    >
      <img
        :src="item.url"
        :alt="item.name"
        class="h-96 w-full object-contain"
      />

      <h3 class="text-center">
        {{ item.name }}
      </h3>
    </UCarousel>

    <div class="mt-4 flex gap-2">
      <button
        v-for="(image, index) in images"
        :key="image.url"
        type="button"
        :class="{ 'opacity-50': activeIndex !== index }"
        @click="selectImage(index)"
      >
        <img
          :src="image.url"
          :alt="image.name"
          class="size-20 object-contain"
        />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
type CarouselImage = {
  url: string;
  name: string;
};

defineProps<{
  images: CarouselImage[];
}>();

const carousel = useTemplateRef("carousel");
const activeIndex = ref(0);

function selectImage(index: number) {
  activeIndex.value = index;
  carousel.value?.emblaApi?.scrollTo(index);
}
</script>
