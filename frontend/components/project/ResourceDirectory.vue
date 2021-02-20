<template>
  <v-card class="px-6 py-3">
    <v-row>
      <ApolloQuery
        :query="require('./../../graphql/project/GetSingleProject.graphql')"
        :variables="{ id: projectId }"
      >
        <template v-slot="{ result: { error, data }, isLoading }">
          <div v-if="isLoading" class="d-flex justify-center">
            <v-progress-circular
              :size="50"
              color="primary"
              indeterminate
            />
          </div>

          <!-- Error -->
          <div v-else-if="error">
            An error occurred
          </div>

          <div v-else-if="data && data.projects_by_pk">
            <v-col>
              <span class="section-title">{{ data.projects_by_pk.title }}</span>
            </v-col>
          </div>
        </template>
      </ApolloQuery>
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
              <v-list-item v-for="options in BUTTON_OPTIONS" :key="options.title" link @click="options.action">
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
              <Resource v-for="folder in foldersInCurrentDirectory" :key="folder.id" :resource="folder" resourceType="folder"/>
            </v-container>
          </v-col>
        </v-row>
        <v-row v-if="filesInCurrentDirectory.length > 0">
          <v-col class="pt-0">
            <v-subheader>Files</v-subheader>
            <v-container class="d-flex flex-wrap pa-0" fluid>
              <Resource v-for="file in filesInCurrentDirectory" :key="file.id" :resource="file" resourceType="file"/>
            </v-container>
          </v-col>
        </v-row>
        <v-row>
          <template>
            <v-btn id="signout-btn" color="danger" style="margin-left: 25px" @click="signOutFunction">
              Sign Out
            </v-btn>
            <v-btn>
              <input id="files" name="file" type="file" multiple>
            </v-btn>
            <v-btn id="signout-btn" color="primary" style="margin-left: 25px" @click="upload">
              Upload
            </v-btn>
            <v-btn id="signout-btn" color="primary" style="margin-left: 25px" @click="getProjectFolder">
              Test
            </v-btn>
          </template>
        </v-row>
      </v-container>
    </v-row>
    <NewFolderModal :isOpen="addFolderOverlay" @closeForm="addFolderOverlay = false" />
  </v-card>
</template>
<script>
import Empty from './resources/Empty'
import Resource from './resources/Resource'
const SCOPE = 'https://www.googleapis.com/auth/drive'
const discoveryUrl = 'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'

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
      parent: [],
      children: [],
      projectId: this.$route.query.id,
      isLoading: false,
      addFolderOverlay: false,
      BUTTON_OPTIONS: [
        { title: 'Add Folder', icon: 'mdi-folder-plus', action: () => { this.addFolderOverlay = !this.addFolderOverlay } },
        { title: 'Upload File/Folder', icon: 'mdi-upload', action: () => { console.log('hi') } }
      ],
      currentDirectory: '/',
      resources: this.BASE_RESOURCE
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

    // setTimeout(this.getProjectResources, 2000)

    // this.getProjectResources()
  },
  methods: {
    // async getProjectResources () {
    //   this.resources = this.BASE_RESOURCE
    //   this.isLoading = true
    //   try {
    //     const response = await this.$axios.get(`${process.env.BASE_API_URL}/resources/${this.projectId}`)
    //     this.resources = response.data.resources
    //   } catch (error) {
    //     this.resources = this.BASE_RESOURCE
    //   } finally {
    //     this.isLoading = false
    //   }
    // },
    handleClientLoad () {
      window.gapi.load('client:auth2', this.initClient)
    },
    initClient () {
      const vm = this
      try {
        window.gapi.client.init({
          apiKey: 'AIzaSyC8i6kIbnt-puBewWgMhiOKxW8V_nNf0xY', // apiKey can be configured to only allow certain websites to call it, so should be fine exposing it.
          clientId: '398518899210-p6bec3lrgqpob9dhj04kjivhdo9kplc2.apps.googleusercontent.com',
          scope: 'https://www.googleapis.com/auth/drive',
          discoveryDocs: [discoveryUrl]
        }).then(() => {
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
      if (!user.uc == null) {
        this.upload()
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
          if (response.capabilities === null || response.capabilities === undefined) {
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
    upload  () {
      if (this.googleAuth === undefined || this.googleAuth == null) {
        this.signInFunction()
        return
      }
      const user = this.googleAuth.currentUser.get()
      // Checks if user has a google log in session in the web app
      if (user.uc == null) {
        this.signInFunction()
      } else {
        const parentId = '15zTqofHz34QuOCXB4_XZXX55aLtEF-eZ' // parent Id of folder to upload file in
        const isAnEditor = this.checkIfEditor(parentId)
        const isAuthorized = user.hasGrantedScopes(SCOPE)
        if (isAnEditor && isAuthorized) {
          // Iterating through the inputted files, as multi upload is allowed
          const f = document.getElementById('files');
          [...f.files].forEach((file, i) => {
            const fr = new FileReader()

            fr.onload = (e) => {
              const data = e.target.result.split(',')
              const obj = { fileName: f.files[i].name, mimeType: data[0].match(/:(\w.+);/)[1], data: data[1] }
              const contentType = obj.mimeType

              const boundary = '287032381131322'
              const delimiter = '\r\n--' + boundary + '\r\n'
              const closeDelim = '\r\n--' + boundary + '--'
              const fileData = obj.data
              const metadata = {
                name: obj.fileName,
                mimeType: contentType,
                parents: [parentId] // Fill in folder_id where the file should be uplaoded to, can only input ONE parent (altho it expects a list)
              }

              const multipartRequestBody =
          delimiter +
          'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
          JSON.stringify(metadata) +
          delimiter +
          'Content-Type: ' + contentType + '\r\n' +
          'Content-Transfer-Encoding: ' + ' base64' + '\r\n\r\n' +
          fileData + '\r\n' +
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
              request.execute(function (file) {
                console.log(file)
              })
            }
            fr.readAsDataURL(file)
          })
        } else {
          console.log('unauthorized')
        }
      }
    },
    async getProjectFolder () {
      this.isLoading = true
      const projectTitle = this.project.title
      try {
        const rootFolder = await this.$axios.post('https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev', {})
        if (rootFolder.data.status === 'success') {
          const projFolder = rootFolder.data.files.find((obj) => {
            return obj.name === projectTitle
          })
          this.parent = projFolder
          this.getChildrenFolder(projFolder.id)
        } else {
          console.log('error')
          // error snackbar popup
        }
      } catch (e) {
        // error snackbar popup
        console.log(e)
      }
      this.isLoading = false
    },
    async getChildrenFolder (folderId) {
      this.isLoading = true
      try {
        const childrenFiles = await this.$axios.post('https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev', { parent_folder: folderId })
        this.children = childrenFiles.data.files
      } catch (e) {
        // error snackbar popup
        console.log(e)
      }
      this.isLoading = false
    }
  }
}
</script>
