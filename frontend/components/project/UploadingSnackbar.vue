<template>
  <v-snackbar
    :timeout="-1"
    v-model="isOpen"
    right
    class="uploadingSnackbar"
  >
    <div class="uploadingSnackbarHeader pa-3">
      <span>Uploading Files</span>
      <v-btn
        @click="isOpen = false"
        dark
        small
        icon
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>
    <div class="uploadingSnackbarContents">
      <v-list light dense>
        <v-list-item v-for="(item, index) in uploadingItems" v-bind:key="index">
          <v-list-item-avatar size="25">
            <v-icon>
              mdi-file
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content class="uploadingFileContent">
            <v-list-item-title class="d-block">{{ item.filename }}</v-list-item-title>
            <v-icon v-if="item.completed" class="d-block" color="success">mdi-check-circle</v-icon>
            <v-progress-circular v-else indeterminate size="25" color="primary"></v-progress-circular>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>
  </v-snackbar>
</template>
<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isOpen: this.value,
      uploadingItems: []
    }
  },
  created () {
    this.$nuxt.$on('uploadingFile', (item) => {
      this.uploadingItems = [item, ...this.uploadingItems]
    })
    this.$nuxt.$on('uploadingCompleted', (filename) => {
      for (let i = this.uploadingItems.length - 1; i >= 0; i--) {
        if (this.uploadingItems[i].filename === filename && !this.uploadingItems[i].completed) {
          this.uploadingItems[i].completed = true
          break
        }
      }
    })
  },
  watch: {
    isOpen: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    },
    value: {
      handler (newValue, oldValue) {
        this.isOpen = this.value
      }
    }
  }
}
</script>
<style>
.uploadingSnackbar > .v-snack__wrapper > .v-snack__content {
  padding: 0 !important;
}
.uploadingSnackbar > .v-snack__wrapper {
  display: block;
}
.uploadingSnackbarHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 48px;
}
.uploadingSnackbarContents {
  background-color: white;
  border-radius: 0 0 4px 4px;
}
.uploadingFileContent{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.uploadingFileContent > * {
  flex: initial;
}
</style>
