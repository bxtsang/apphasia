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
          </template>
        </v-row>
      </v-container>
    </v-row>
  </v-card>
</template>
<script>
import Empty from './resources/Empty'
import ResourceFile from './resources/ResourceFile'
import ResourceFolder from './resources/ResourceFolder'

const SCOPE = 'https://www.googleapis.com/auth/drive'
const discoveryUrl = 'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'

export default {
  components: { Empty, ResourceFile, ResourceFolder },
  data () {
    return {
      isLoading: true,
      projectId: this.$route.query.id,
      access_token: '',
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
    const script = document.createElement('script')
    script.onload = this.handleClientLoad
    script.src = 'https://apis.google.com/js/api.js'
    document.body.appendChild(script)
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
    },
    handleClientLoad () {
      window.gapi.load('client:auth2', this.initClient)
    },
    initClient () {
      const vm = this
      try {
        window.gapi.client.init({
          apiKey: 'AIzaSyC8i6kIbnt-puBewWgMhiOKxW8V_nNf0xY',
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
    upload  () {
      const user = this.googleAuth.currentUser.get()
      console.log(user)
      if (user.uc == null) {
        this.signInFunction()
      } else {
        const isAuthorized = user.hasGrantedScopes(SCOPE)
        console.log(isAuthorized)
        if (isAuthorized) {
          const f = document.getElementById('files')
          console.log(f);
          [...f.files].forEach((file, i) => {
            const fr = new FileReader()
            // var fileContent2 = fr.readAsText(f.files[i])

            fr.onload = (e) => {
              console.log(e.target.result)
              const data = e.target.result.split(',')
              const obj = { fileName: f.files[i].name, mimeType: data[0].match(/:(\w.+);/)[1], data: data[1] }
              // const content = new Blob([obj.data])
              const contentType = obj.mimeType

              const boundary = '287032381131322'
              const delimiter = '\r\n--' + boundary + '\r\n'
              const closeDelim = '\r\n--' + boundary + '--'
              const fileData = obj.data
              const metadata = {
                name: obj.fileName,
                mimeType: contentType,
                parents: ['']
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

              console.log(multipartRequestBody)
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
    }
  }
}
</script>
