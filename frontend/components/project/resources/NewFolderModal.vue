<template>
  <v-dialog
      v-model="isOpen"
      width="500"
    >
      <v-card class="pa-8">
        <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="createNewFolder">
          <v-container class="pa-0">
            <v-row>
              <v-col class="py-0">
                <span class="section-title">Add Folder</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <v-text-field
                  v-model="folderName"
                  label="Folder Name"
                  :rules="[v => !!v || 'Folder Name is required']"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0 d-flex justify-end">
                <v-btn type="submit" color="primary">Save</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      valid: true,
      folderName: ''
    }
  },
  methods: {
    createNewFolder () {
      if (this.$refs.form.validate()) {
        console.log(`upload new folder ${this.folderName}`)
        // CALL API HERE

        this.folderName = ""
        this.isOpen = false
      }
    }
  }
}
</script>
