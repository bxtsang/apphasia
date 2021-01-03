<template>
  <v-col class="d-flex justify-center">
    <div class="circle">
      <v-icon x-large color="#D4D4D4">mdi-folder-upload</v-icon>
      <span class="title">Drop files here</span>
      <span class="subtitle">or use the "New" Button</span>
    </div>
  </v-col>
</template>
<style scoped>
.circle {
  height: 250px;
  width: 250px;
  border-radius: 100vh;
  background-color: #F8F8F8;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.circle .subtitle {
  font-size: 16px;
}
</style>
