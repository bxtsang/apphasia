<template>
  <v-card class="px-6 py-3">
    <v-row>
      <v-col>
        <span class="section-title">Project Name</span>
      </v-col>
      <v-col class="d-flex justify-end">
        <div class="text-center">
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" v-bind="attrs" v-on="on">
                <v-icon left>
                  mdi-plus
                </v-icon>
                New
              </v-btn>
            </template>
            <v-list>
              <v-list-item v-for="options in BUTTON_OPTIONS" :key="options.title" link>
                <v-icon left>
                  {{ options.icon }}
                </v-icon>
                <v-list-item-title>{{ options.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </v-col>
    </v-row>
    <v-row v-if="isLoading">
      <v-col class="d-flex justify-center">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        />
      </v-col>
    </v-row>
    <v-row v-else-if="filesInCurrentDirectory.length == 0 && foldersInCurrentDirectory.length == 0">
      <Empty />
    </v-row>
    <v-row v-else>
      <v-container class="pa-0" fluid>
        <v-row v-if="foldersInCurrentDirectory.length > 0">
          <v-col class="pt-0">
            <v-subheader>Folders</v-subheader>
            <v-container class="d-flex flex-wrap pa-0" fluid>
              <ResourceFolder />
            </v-container>
          </v-col>
        </v-row>
        <v-row v-if="filesInCurrentDirectory.length > 0">
          <v-col class="pt-0">
            <v-subheader>Files</v-subheader>
            <v-container class="d-flex flex-wrap pa-0" fluid>
              <ResourceFile />
            </v-container>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
  </v-card>
</template>
<script>
import Empty from './resources/Empty'
import ResourceFile from './resources/ResourceFile'
import ResourceFolder from './resources/ResourceFolder'

export default {
  components: { Empty, ResourceFile, ResourceFolder },
  data () {
    return {
      isLoading: true,
      projectId: this.$route.query.id,
      BASE_RESOURCE: {
        directory: '/',
        folders: [],
        files: []
      },
      BUTTON_OPTIONS: [
        { title: 'Add Folder', icon: 'mdi-folder-plus', action: () => { console.log('hi') } },
        { title: 'Upload File/Folder', icon: 'mdi-upload', action: () => { console.log('hi') } }
      ],
      currentDirectory: '/',
      resources: this.BASE_RESOURCE
    }
  },
  computed: {
    filesInCurrentDirectory () {
      return [
        {
          id: '',
          name: '',
          type: 'pdf'
        }
      ]
    },
    foldersInCurrentDirectory () {
      return [
        {
          name: 'forms'
        }
      ]
    }
  },
  mounted () {
    setTimeout(this.getProjectResources, 2000)
    // this.getProjectResources()
  },
  methods: {
    async getProjectResources () {
      this.resources = this.BASE_RESOURCE
      this.isLoading = true
      try {
        const response = await this.$axios.get(`${process.env.BASE_API_URL}/resources/${this.projectId}`)
        this.resources = response.data.resources
      } catch (error) {
        this.resources = this.BASE_RESOURCE
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
