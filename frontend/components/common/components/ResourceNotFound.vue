<template>
  <div class="d-flex justify-center flex-column text-center not-found-container">
    <h1 class="mb-4">Resource Not Found</h1>
    <v-img src="/undraw_404.svg" contain/>
    <h2 class="mt-4">The Resource might be Deleted</h2>
    <NuxtLink to="/">
      Home page
    </NuxtLink>
  </div>
</template>
<style scoped>
.not-found-container{
  max-width: 500px;
  margin: auto;
}
</style>
