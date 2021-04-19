<template>
  <div class="d-flex justify-center flex-column text-center not-found-container">
    <h1 class="mb-4">Sorry, we can't find what you're looking for!</h1>
    <div class="ma-auto image-container">
      <img src="/undraw_404.svg"/>
    </div>
    <h3 class="mt-4">The resource might have been deleted or removed</h3>
    <NuxtLink to="/">
      Back to Dashboard
    </NuxtLink>
  </div>
</template>
<style scoped>
.not-found-container{
  margin: auto;
}
.image-container{
  max-width: 500px;
}
.image-container img{
  width: 100%;
}
</style>
