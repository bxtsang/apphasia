<template>
  <div>
    <!-- Item Card Folder-->
    <v-card
      v-if="resourceType === 'folder'"
      class="ma-2 d-flex align-center clickable"
      outlined
      width="200"
      @contextmenu="show"
    >
      <v-icon class="ma-4">
        mdi-folder
      </v-icon>
      <span> {{ resource.name }}</span>
    </v-card>

    <!-- Item Card File-->
    <v-card
      v-else
      class="pa-3 ma-2 d-flex flex-column align-center clickable"
      outlined
      width="200"
      @contextmenu="show"
    >
      <v-icon x-large class="ma-4">
        mdi-file
      </v-icon>
      <span> {{ resource.name }} </span>
    </v-card>

    <!-- Context Menu -->
    <v-menu
      v-model="showMenu"
      :position-x="x"
      :position-y="y"
      absolute
      offset-y
      transition="scale-transition"
    >
      <v-list dense>
        <v-list-item
          v-for="(item, index) in RIGHT_CLICK_OPTIONS"
          :key="index"
          link
          @click="item.action"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
export default {
  props: {
    resourceType: {
      type: String,
      default: 'file'
    },
    resource: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      showMenu: false,
      x: 0,
      y: 0,
      RIGHT_CLICK_OPTIONS: [
        { title: 'Delete', icon: 'mdi-delete', action: this.deleteResource }
      ]
    }
  },
  mounted () {
    if (this.resource.webContentLink) {
      this.RIGHT_CLICK_OPTIONS.push({ title: 'Download', icon: 'mdi-download', action: this.downloadResource })
    }
  },
  methods: {
    show (e) {
      e.preventDefault()
      this.showMenu = false
      this.x = e.clientX
      this.y = e.clientY
      this.$nextTick(() => {
        this.showMenu = true
      })
    },
    downloadResource () {
      window.location.href = this.resource.webContentLink
    },
    async deleteResource () {
      try {
        const rootFolder = await this.$axios.post('https://schwn3irr1.execute-api.ap-southeast-1.amazonaws.com/dev', { file_id: this.resource.id })
        if (rootFolder.data.status !== 'success') {
          console.log('error')
          // insert error snackbar here
        } else {
          console.log('success!')
          this.$emit('refresh')
        }
      } catch (e) {
        console.log(e)
        // insert error snackbar here
      }
    }
  }
}
</script>
<style scoped>
.clickable {
  cursor: pointer;
}
</style>
