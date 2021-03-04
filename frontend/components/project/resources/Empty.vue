<template>
  <v-col class="d-flex justify-center">
    <div class="circle">
      <v-icon x-large color="#D4D4D4">
        mdi-folder-upload
      </v-icon>
      <div v-if="folderExist" class="d-flex flex-column text-center">
        <span class="title">Folder empty</span>
        <span class="subtitle">Use the "New" Button</span>
      </div>
      <div v-else class="text-center">
        <span class="subtitle">Folder does not exist on Google Drive</span>
      </div>
    </div>
  </v-col>
</template>
<script>
export default {
  props: {
    folderExist: {
      type: Boolean,
      default: false
    }
  },
  mounted () {
    console.log('inside resource: ' + this.folderExist)
  }
}
</script>
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
