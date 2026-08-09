<template>
  <main class="mt-28 flex justify-center px-6">
    <div class="max-w-xl text-center">
      <h1 class="text-4xl font-bold">
        Welcome to the <br />
        Art Commission Platform
      </h1>
      <p class="mt-4 mb-6 text-lg text-gray-600">
        Discover artists and bring your ideas to life.
      </p>
      <NuxtLink to="/explore">
        <Button label="Start exploring">
          <template #icon>
            <Icon name="material-symbols:arrow-forward" class="size-4" />
          </template>
        </Button>
      </NuxtLink>
    </div>
  </main>
</template>
