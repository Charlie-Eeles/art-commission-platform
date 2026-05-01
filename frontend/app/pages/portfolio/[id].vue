<template>
  <div>
    <div class="mx-auto w-fit">
      <h2 class="mb-4 text-2xl font-bold">
        Welcome to the Art Commission Platform portfolio for
        {{ route.params.id }}!
      </h2>

      <PortfolioCarousel :images="images" />
    </div>
  </div>
</template>

<script setup lang="ts">
import bustExample from "~/assets/dev/bust-example.jpg";
import colourExample from "~/assets/dev/colour-example.jpg";
import fullBodyExample from "~/assets/dev/full-body-example.jpg";

const route = useRoute();

const images = [
  { url: colourExample, name: "Full colour drawing" },
  { url: fullBodyExample, name: "Full body b/w drawing" },
  { url: bustExample, name: "Simple b/w drawing" },
];
</script>
