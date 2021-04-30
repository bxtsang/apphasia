<template>
  <div>
    <!-- Item Card Folder-->
    <v-card
      v-if="resourceType === 'folder'"
      class="ma-2 d-flex align-center clickable"
      outlined
      width="270"
      @contextmenu="show"
      @dblclick="changeDirectory"
    >
      <v-icon class="ma-4">
        mdi-folder
      </v-icon>
      <span> {{ resource.name }}</span>
    </v-card>

    <!-- Item Card File-->
    <v-card
      v-else
      class="ma-2 pt-2 d-flex flex-column justify-space-between align-center clickable"
      outlined
      height="220"
      width="270"
      @contextmenu="show"
      @dblclick="changeDirectory"
    >
      <v-img
        v-if="authorizedResourcesMimeType.includes(resource.mimeType)"
        :src="resource.iconLink"
        contain
        height="30"
        width="30"
      />
      <v-img v-else :src="resource.thumbnailLink" height="120" />
      <v-card-actions>
        <span> {{ resource.name }}</span>
      </v-card-actions>
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
    },
    accessToken: {
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
      ],
      authorizedResourcesMimeType: [
        'application/vnd.google-apps.audio',
        'application/vnd.google-apps.document',
        'application/vnd.google-apps.drive-sdk',
        'application/vnd.google-apps.drawing',
        'application/vnd.google-apps.file',
        'application/vnd.google-apps.folder',
        'application/vnd.google-apps.form',
        'application/vnd.google-apps.fusiontable',
        'application/vnd.google-apps.map',
        'application/vnd.google-apps.photo',
        'application/vnd.google-apps.presentation',
        'application/vnd.google-apps.script',
        'application/vnd.google-apps.shortcut',
        'application/vnd.google-apps.site',
        'application/vnd.google-apps.spreadsheet',
        'application/vnd.google-apps.unknown',
        'application/vnd.google-apps.video'
      ]
    }
  },
  created () {
    this.$nuxt.$on('open-menu', (id) => {
      if (id !== this.resource) {
        this.showMenu = false
      }
    })
  },
  mounted () {
    if (this.resource.webContentLink) {
      this.RIGHT_CLICK_OPTIONS.push({
        title: 'Download',
        icon: 'mdi-download',
        action: this.downloadResource
      })
    }

    if (this.resource.webViewLink) {
      this.RIGHT_CLICK_OPTIONS.push({
        title: 'Open in drive',
        icon: 'mdi-google-drive',
        action: this.openInDrive
      })
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
      this.$nuxt.$emit('open-menu', this.resource.id)
    },
    downloadResource () {
      window.location.href = this.resource.webContentLink
    },
    deleteResource () {
      this.$emit('deleteResource')
    },
    openInDrive () {
      window.open(this.resource.webViewLink, '_blank')
    },
    changeDirectory () {
      this.$emit('changeDirectory')
    }
  }
}
</script>
<style scoped>
.clickable {
  cursor: pointer;
}
</style>
