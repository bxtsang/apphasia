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

        <!-- General Section -->

        <v-row>
          <v-col class="py-0" cols="12" lg="6">
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
            <v-row>
              <v-col class="py-0">
                <v-switch
                  v-model="projectData.is_recurring"
                  label="Is Recurring?"
                />
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
                  v-model="projectData.owner"
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
                <ProjectPersonMultiSelector
                  v-model="projectData.volunteers.data"
                  label="Volunteers Involved"
                  type="volunteers"
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
              <v-row>
                <!-- <DeleteResourceModal
                  v-if="$auth.user['custom:role'] === 'core_team' && pwa"
                  :resource="pwa"
                  :resourceType="'pwas'"
                  @deleteSuccess="$emit('closeForm')"
                /> -->
                <v-spacer/>
                <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
                  {{ project ? 'Edit' : 'Save' }}
                </v-btn>
              </v-row>
            </v-row>
          </v-col>

          <v-divider class="mx-6" vertical/>

          <!-- Assignment Section -->
          <v-col cols="12" lg="6">

          </v-col>
        </v-row>
        <!-- <pre>{{ projectData }}</pre> -->
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
import CreateProject from './../../graphql/project/CreateProject.graphql'

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
        is_recurring: false,
        staffs: { data: [] },
        volunteers: { data: [] },
        pwas: { data: [] },
        owner: -1
      }
    }
  },
  computed: {
    formSubmitMethod () {
      if (this.pwa) {
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
        this.$apollo.mutate({
          mutation: CreateProject,
          variables: { project: newProjectData }
          // update: (store, { data: { insert_pwas_one: newPWA } }) => {
          //   const data = store.readQuery({ query: GetAllPWA })
          //   data.pwas.push(newPWA)
          //   store.writeQuery({ query: GetAllPWA, data })
          // }
        }).then((data) => {
          this.isSubmitting = false
          // this.projectData = {}
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Project successfully created', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    editProject () {

    }
  }
}
</script>
