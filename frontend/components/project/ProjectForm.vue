<template>
  <v-card class="pa-8">
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="formSubmitMethod">
      <v-container class="pa-0">
        <v-row>
          <v-col class="py-0">
            <span v-if="project" class="section-title">Edit Project</span>
            <span v-else class="section-title">Add Project</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">Project Details</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <ProjectNameInput v-model="projectData.title"/>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <ProjectNotesInput v-model="projectData.description"/>
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">People Involved</span>
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col class="py-0">
                <ProjectStaffSelector
                  v-model="projectData.owner_id"
                  label="Staff In-Charge"
                />
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col class="py-0">
                <ProjectPersonMultiSelector
                  v-model="projectData.staffs.data"
                  label="Staff Involved"
                  type="staffs"
                />
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col class="py-0">
                <ProjectVolTypesInput
                  v-model="projectData.voltypes"
                />
              </v-col>
            </v-row>
            <v-row class="mt-3" v-if="projectData.voltypes !== ''">
              <v-col class="py-0">
                <ProjectPersonMultiSelector
                  v-model="projectData.volunteers.data"
                  label="Volunteers Involved"
                  type="volunteers"
                  :voltype="projectData.voltypes"
                />
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col class="py-0">
                <ProjectPersonMultiSelector
                  v-model="projectData.pwas.data"
                  label="PWAs Involved"
                  type="pwas"
                />
              </v-col>
            </v-row>
            <v-row>
              <div class="my-3 ml-3">
                <DeleteResourceModal
                  v-if="$auth.user['custom:role'] === 'core_team' && project"
                  :resource="project"
                  :resourceType="'projects'"
                  @deleteSuccess="$emit('closeForm')"
                />
              </div>
              <v-spacer/>
              <v-btn color="primary" class="my-3 mr-3" type="submit" :loading="isSubmitting">
                {{ project ? 'Edit' : 'Save' }}
              </v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
import CreateProject from './../../graphql/project/CreateProject.graphql'
import GetAllProject from './../../graphql/project/GetAllProject.graphql'
import UpdateProject from './../../graphql/project/UpdateProject.graphql'
import GetSingleProject from './../../graphql/project/GetSingleProject.graphql'

export default {
  props: {
    project: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false,
      projectData: {
        title: this.project ? this.project.title : '',
        description: this.project ? this.project.description : '',
        staffs: { data: this.project ? this.project.staffs.map(item => item.staff.id) : [] },
        volunteers: { data: this.project ? this.project.volunteers.map(item => item.volunteer.general_info.id) : [] },
        pwas: { data: this.project ? this.project.pwas.map(item => item.pwa.general_info.id) : [] },
        owner_id: this.project ? this.project.owner.id : -1,
        voltypes: this.project ? this.project.voltypes : 'Project_Volunteer'
      }
    }
  },
  computed: {
    formSubmitMethod () {
      if (this.project) {
        return this.editProject
      } else {
        return this.submitProject
      }
    }
  },
  methods: {
    submitProject () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const _ = require('lodash')
        const newProjectData = _.cloneDeep(this.projectData)
        newProjectData.staffs.data = this.projectData.staffs.data.map((item) => { return { staff_id: item } })
        newProjectData.volunteers.data = this.projectData.volunteers.data.map((item) => { return { vol_id: item } })
        newProjectData.pwas.data = this.projectData.pwas.data.map((item) => { return { pwa_id: item } })
        this.$apollo.mutate({
          mutation: CreateProject,
          variables: { project: newProjectData },
          update: (store, { data: { insert_projects_one: newProject } }) => {
            this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
            this.createGDriveFolder(newProjectData.title)
          }
        }).then((data) => {
          this.isSubmitting = false
          this.projectData = {
            title: '',
            description: '',
            staffs: { data: [] },
            volunteers: { data: [] },
            pwas: { data: [] },
            owner_id: -1,
            voltypes: 'Project_Volunteer'
          }
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Project successfully created', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    editProject () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const _ = require('lodash')
        const newProjectData = _.cloneDeep(this.projectData)
        newProjectData.staffs.data = this.projectData.staffs.data.map((item) => { return { staff_id: item } })
        newProjectData.volunteers.data = this.projectData.volunteers.data.map((item) => { return { vol_id: item } })
        newProjectData.pwas.data = this.projectData.pwas.data.map((item) => { return { pwa_id: item } })
        newProjectData.id = this.project.id
        newProjectData.pwa_assigned_vols = {
          data: this.project.pwa_assigned_vols.map((item) => {
            return {
              pwa_id: item.pwa.general_info.id,
              vol_id: item.volunteer.general_info.id
            }
          }).filter((item) => {
            return this.projectData.volunteers.data.includes(item.vol_id) && this.projectData.pwas.data.includes(item.pwa_id)
          })
        }
        newProjectData.pwa_assigned_staffs = {
          data: this.project.pwa_assigned_staffs.map((item) => {
            return {
              pwa_id: item.pwa.general_info.id,
              staff_id: item.staff.id
            }
          }).filter((item) => {
            return this.projectData.staffs.data.includes(item.staff_id) && this.projectData.pwas.data.includes(item.pwa_id)
          })
        }
        this.$apollo.mutate({
          mutation: UpdateProject,
          variables: { id: this.project.id, project: newProjectData },
          update: (store, { data: { insert_projects_one: updatedProject } }) => {
            this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
          }
        }).then((data) => {
          this.isSubmitting = false
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Project successfully updated', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    createGDriveFolder (folderName) {
      const postHeader = {
        'Content-Type': 'application/json'
      }
      const postBody = {
        new_folder: folderName
      }
      this.$axios.post(
        'https://67sbpripz3.execute-api.ap-southeast-1.amazonaws.com/dev',
        JSON.stringify(postBody),
        { postHeader }
      ).then((res) => {
        console.log(res)
      })
    }
  },
  watch: {
    'projectData.voltypes': {
      handler (newValue, oldValue) {
        this.projectData.volunteers.data = []
      }
    }
  }
}
</script>
