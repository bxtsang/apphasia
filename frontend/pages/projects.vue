<template>
  <div>
    <IndividualProjectView v-if="projectId" />
    <v-container v-else class="pa-0" fluid>
      <v-row>
        <v-col>
          <NewProjectModal />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card class="px-6 py-3">
            <h1 class="title">Projects</h1>
            <v-row>
              <v-col v-if="isLoading" class="d-flex justify-center">
                <v-progress-circular
                  :size="50"
                  color="primary"
                  indeterminate
                />
              </v-col>
              <v-col v-for="(project, index) in projects" v-else :key="index" cols="6">
                <Project :project="project" />
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import Project from '../components/projects/Project'
import IndividualProjectView from '../components/projects/IndividualProjectView'
import NewProjectModal from '../components/projects/modals/NewProjectModal'

export default {
  components: { Project, IndividualProjectView, NewProjectModal },
  data () {
    return {
      isLoading: true,
      projectId: this.$route.query.id,
      projects: []
    }
  },
  watch: {
    '$route.query.id': {
      handler () {
        this.projectId = this.$route.query.id
      }
    }
  },
  mounted () {
    setTimeout(this.getProjects, 2000)
    // this.getProjects()
  },
  methods: {
    async getProjects () {
      this.projects = []
      this.isLoading = true
      try {
        const response = await this.$axios.get(`${process.env.BASE_API_URL}/projects`)
        this.projects = response.data
      } catch (error) {
        this.projects = []
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
