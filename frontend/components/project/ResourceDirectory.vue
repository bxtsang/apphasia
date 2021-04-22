<template>
  <v-card>
    <v-row>
      <ApolloQuery
        :query="require('./../../graphql/project/GetSingleProject.graphql')"
        :variables="{ id: projectId }"
        class="d-flex justify-start align-center col-8"
      >
        <template v-slot="{ result: { error, data }, isLoading }">
          <div v-if="isLoading" class="d-flex justify-center pa-6">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </div>

          <!-- Error -->
          <div v-else-if="error">
            An error occurred
          </div>

          <div v-else-if="data && data.projects_by_pk">
            <v-breadcrumbs large :items="paths" class="pl-0">
              <template v-slot:divider>
                <v-icon>mdi-chevron-right</v-icon>
              </template>
              <v-breadcrumbs-item
                slot="item"
                slot-scope="{ item }"
                class="breadcrumbsItem"
                @click="changeDirectory(item.id, item.text)"
              >
                {{ item.text }}
              </v-breadcrumbs-item>
            </v-breadcrumbs>
          </div>
        </template>
      </ApolloQuery>
      <v-col class="d-flex justify-end align-center col-4">
        <div class="text-center">
          <v-btn color="" class="mr-4" @click="refresh(currentFolder.id)">
            refresh
          </v-btn>
        </div>
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
              <v-list-item
                v-for="options in BUTTON_OPTIONS"
                :key="options.title"
                link
                @click="options.action"
              >
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

    <v-row v-if="loading">
      <v-col class="d-flex justify-center">
        <v-progress-circular :size="50" color="primary" indeterminate />
      </v-col>
    </v-row>
    <v-row
      v-else-if="
        filesInCurrentDirectory.length == 0 &&
          foldersInCurrentDirectory.length == 0
      "
    >
      <Empty :folder-exist="folderExist" />
    </v-row>
    <v-row v-else>
      <v-container class="pa-0" fluid>
        <v-row v-if="foldersInCurrentDirectory.length > 0">
          <v-col class="pt-0">
            <v-subheader>Folders</v-subheader>
            <v-container class="d-flex flex-wrap pa-0 px-3" fluid>
              <Resource
                v-for="folder in foldersInCurrentDirectory"
                :key="folder.id"
                :resource="folder"
                resource-type="folder"
                @deleteResource="deleteResource(folder.id)"
                @refresh="refreshWithDelay(parent.id)"
                @changeDirectory="changeDirectory(folder.id, folder.name)"
              />
            </v-container>
          </v-col>
        </v-row>
        <v-row v-if="filesInCurrentDirectory.length > 0">
          <v-col class="pt-0">
            <v-subheader>Files</v-subheader>
            <v-container class="d-flex flex-wrap px-2" fluid>
              <Resource
                v-for="file in filesInCurrentDirectory"
                :key="file.id"
                :resource="file"
                resource-type="file"
                @refresh="refreshWithDelay(parent.id)"
                @deleteResource="deleteFile(file.id)"
                @changeDirectory="openFile(file.webViewLink)"
              />
            </v-container>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
    <NewFolderModal
      :is-open="addFolderOverlay"
      :parent-id="currentFolder.id"
      @closeForm="addFolderOverlay = false"
      @refresh="refreshWithDelay(currentFolder.id)"
    />
    <UploadingSnackbar v-model="showUpload" />
    <input
      id="files"
      name="file"
      type="file"
      multiple
      hidden
      @change="upload"
    >
  </v-card>
</template>
<script>
import Empty from './resources/Empty'
import Resource from './resources/Resource'
const SCOPE = 'https://www.googleapis.com/auth/drive'
const discoveryUrl =
  'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'

export default {
  components: { Empty, Resource },
  props: {
    project: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      paths: [],
      parent: [],
      currentFolder: '',
      children: [],
      projectId: this.$route.query.id,
      loading: false,
      addFolderOverlay: false,
      folderExist: false,
      BUTTON_OPTIONS: [
        {
          title: 'Add Folder',
          icon: 'mdi-folder-plus',
          action: () => {
            this.addFolderOverlay = !this.addFolderOverlay
          }
        },
        {
          title: 'Upload File/Folder',
          icon: 'mdi-upload',
          action: () => {
            document.getElementById('files').click()
          }
        }
      ],
      currentDirectory: '/',
      resources: this.BASE_RESOURCE,
      showUpload: false
    }
  },
  computed: {
    filesInCurrentDirectory () {
      const children = this.children
      return children.filter((obj) => {
        return obj.mimeType !== 'application/vnd.google-apps.folder'
      })
    },
    foldersInCurrentDirectory () {
      const children = this.children
      return children.filter((obj) => {
        return obj.mimeType === 'application/vnd.google-apps.folder'
      })
    }
  },
  mounted () {
    // loads the google api script
    const script = document.createElement('script')
    script.onload = this.handleClientLoad
    script.src = 'https://apis.google.com/js/api.js'
    document.body.appendChild(script)
    this.getProjectFolder()
    console.log(this.folderExist)
  },
  methods: {
    handleClientLoad () {
      window.gapi.load('client:auth2', this.initClient)
    },
    initClient () {
      const vm = this
      try {
        window.gapi.client
          .init({
            apiKey: 'AIzaSyC8i6kIbnt-puBewWgMhiOKxW8V_nNf0xY', // apiKey can be configured to only allow certain websites to call it, so should be fine exposing it.
            clientId:
              '398518899210-p6bec3lrgqpob9dhj04kjivhdo9kplc2.apps.googleusercontent.com',
            scope: 'https://www.googleapis.com/auth/drive',
            discoveryDocs: [discoveryUrl]
          })
          .then(() => {
            vm.googleAuth = window.gapi.auth2.getAuthInstance()
            vm.googleAuth.isSignedIn.listen(vm.updateSigninStatus)
          })
      } catch (e) {
        console.log(e)
      }
    },
    async signInFunction () {
      await this.googleAuth.signIn()
      const user = this.googleAuth.currentUser.get()
      console.log(user)
      if (user != null) {
        console.log('user is not null after signing in')
        this.upload()
      } else {
        console.log('user is null')
      }
    },
    signOutFunction () {
      this.googleAuth.signOut()
    },
    async checkIfEditor (parentId) {
      const request = window.gapi.client.request({
        path: 'https://www.googleapis.com/drive/v3/files/' + parentId,
        method: 'GET',
        params: { fileId: parentId, fields: 'capabilities' }
      })

      try {
        await request.execute(function (response) {
          if (response.error !== null || response.error !== undefined) {
            return false
          }
          if (
            response.capabilities === null ||
            response.capabilities === undefined
          ) {
            return false
          } else {
            console.log(response.capabilities.canAddChildren)
            return response.capabilities.canAddChildren
          }
        })
      } catch (error) {
        console.log(error)
        return false
      }
    },
    async upload () {
      console.log('uploading file')
      const vm = this
      const f = document.getElementById('files')
      if (this.googleAuth === undefined || this.googleAuth == null) {
        console.log('auth instance not initialized')
        this.signInFunction()
      }
      const user = this.googleAuth.currentUser.get()
      // Checks if user has a google log in session in the web app
      if (user == null) {
        console.log('user not signed in')
        this.signInFunction()
      } else {
        const parentId = this.currentFolder.id // parent Id of folder to upload file in
        const isAnEditor = this.checkIfEditor(parentId)
        const isAuthorized = user.hasGrantedScopes(SCOPE)
        if (isAnEditor && isAuthorized) {
          // Iterating through the inputted files, as multi upload is allowed
          this.showUpload = true
          try {
            for (const file of f.files) {
              this.$nuxt.$emit('uploadingFile', { filename: file.name, completed: false })
              await this.uploadHelper(file, parentId)
            }
          } catch (e) {
            vm.error()
            console.log(e)
          } finally {
            vm.refreshWithDelay(parentId)
            f.value = null
          }
        } else {
          vm.error()
          f.value = null
          vm.loading = false
        }
      }
    },
    uploadHelper (file, parentId) {
      console.log('upload helper called')
      const nuxtObject = this.$nuxt
      return new Promise(function (resolve, reject) {
        try {
          const fr = new FileReader()
          fr.onload = async (e) => {
            const data = e.target.result.split(',')
            const obj = {
              fileName: file.name,
              mimeType: data[0].match(/:(\w.+);/)[1],
              data: data[1]
            }
            const contentType = obj.mimeType

            const boundary = '287032381131322'
            const delimiter = '\r\n--' + boundary + '\r\n'
            const closeDelim = '\r\n--' + boundary + '--'
            const fileData = obj.data
            const metadata = {
              name: obj.fileName,
              mimeType: contentType,
              parents: [parentId]
            }

            const multipartRequestBody =
              delimiter +
              'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
              JSON.stringify(metadata) +
              delimiter +
              'Content-Type: ' +
              contentType +
              '\r\n' +
              'Content-Transfer-Encoding: ' +
              ' base64' +
              '\r\n\r\n' +
              fileData +
              '\r\n' +
              closeDelim

            const request = window.gapi.client.request({
              path: 'https://www.googleapis.com/upload/drive/v3/files',
              method: 'POST',
              params: { uploadType: 'multipart' },
              headers: {
                'Content-Type': 'multipart/related; boundary=' + boundary + ''
              },
              body: multipartRequestBody
            })
            await request.execute(function (file) {
              console.log(file)
              nuxtObject.$emit('uploadingCompleted', file.name)
              resolve('success')
            })
          }
          fr.readAsDataURL(file)
        } catch (e) {
          console.log(e)
          reject(e)
        }
      })
    },
    async getProjectFolder () {
      this.loading = true
      const projectTitle = this.project.title
      try {
        const rootFolder = await this.$axios.post(
          'https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev',
          {}
        )
        if (rootFolder.data.status === 'success') {
          const projFolder = rootFolder.data.files.find((obj) => {
            return obj.name === projectTitle
          })
          if (projFolder !== undefined && projFolder !== null) {
            this.parent = projFolder
            this.currentFolder = projFolder
            this.paths.push({ id: projFolder.id, text: projFolder.name })
            this.getChildrenFolder(projFolder.id)
            this.folderExist = true
          } else {
            this.folderExist = false
          }
        } else {
          console.log('error')
          this.error()
        }
      } catch (e) {
        this.error()
        console.log(e)
      }
      console.log('real: ' + this.folderExist)
      this.loading = false
    },
    async getChildrenFolder (folderId) {
      this.loading = true
      try {
        const childrenFiles = await this.$axios.post(
          'https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev',
          { parent_folder: folderId }
        )
        this.children = childrenFiles.data.files
      } catch (e) {
        this.error()
        console.log(e)
      }
      this.loading = false
    },
    refreshWithDelay (newParentId) {
      this.loading = true
      setTimeout(async () => {
        const childrenFiles = await this.$axios.post(
          'https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev',
          { parent_folder: newParentId }
        )
        this.children = childrenFiles.data.files
        this.loading = false
      }, 2000)
    },
    async refresh (newParentId) {
      this.loading = true
      try {
        const childrenFiles = await this.$axios.post(
          'https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev',
          { parent_folder: newParentId }
        )
        this.children = childrenFiles.data.files
      } catch (e) {
        console.log(e)
        this.error()
      }

      this.loading = false
    },
    changeDirectory (folderId, folderName) {
      const paths = this.paths
      const path = { id: folderId, text: folderName }
      const duplicateIndex = this.existsInPaths(folderId)
      if (duplicateIndex !== -1) {
        if (paths.length > 0 && folderId === paths[paths.length - 1].id) {
          console.log(1)
          return
        } else {
          paths.splice(parseInt(duplicateIndex) + 1)
        }
      } else if (folderId === this.parent.id) {
        this.paths = []
      } else {
        paths.push(path)
      }
      this.currentFolder = path
      this.refresh(folderId)
    },
    existsInPaths (folderId) {
      for (const index in this.paths) {
        if (this.paths[index].id === folderId) {
          return index
        }
      }
      return -1
    },
    async deleteResource (fileId) {
      this.loading = true
      const vm = this
      try {
        const rootFolder = await this.$axios.post(
          'https://schwn3irr1.execute-api.ap-southeast-1.amazonaws.com/dev',
          { file_id: fileId }
        )
        if (rootFolder.data.status !== 'success') {
          console.log('error')
          vm.error()
        } else {
          vm.refreshWithDelay(vm.currentFolder.id)
        }
      } catch (e) {
        try {
          const request = window.gapi.client.request({
            path: 'https://www.googleapis.com/drive/v3/files/' + fileId,
            method: 'DELETE',
            params: { fileId }
          })
          await request.execute(function (response) {
            console.log(response)
            if (
              response &&
              (response.error !== null || response.error !== undefined)
            ) {
              vm.error()
            }
            vm.refreshWithDelay(vm.currentFolder.id)
          })
        } catch (e2) {
          console.log(e2)
          vm.error()
        }
        console.log(e)
      }
    },
    async deleteFile (fileId) {
      const vm = this
      try {
        const request = window.gapi.client.request({
          path: 'https://www.googleapis.com/drive/v3/files/' + fileId,
          method: 'DELETE',
          params: { fileId }
        })
        await request.execute(function (response) {
          console.log(response)
          if (
            response &&
            (response.error !== null || response.error !== undefined)
          ) {
            vm.error()
          }
          vm.refreshWithDelay(vm.currentFolder.id)
        })
      } catch (e) {
        vm.error()
        console.log(e)
      }
    },
    openFile (link) {
      window.open(link)
    },
    error () {
      this.$store.commit('notification/newNotification', [
        'Something went wrong, please try again.',
        'error'
      ])
    }
  }
}
</script>

<style>
.breadcrumbsItem {
  cursor: pointer;
}
</style>
