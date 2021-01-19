<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <h1 class="title hover-underline">
          <NuxtLink to="/projects">
            Projects
          </NuxtLink> / {{ project ? project.name : "" }}
        </h1>
        <v-row>
          <v-col lg="6" md="6" sm="12">
            <ProjectDetails :isLoading="isLoading" :project="project" />
          </v-col>
          <v-col lg="6" md="6" sm="12">
            <ProjectTasks />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <ResourceDirectory />
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import ProjectDetails from './ProjectDetails'
import ProjectTasks from './ProjectTasks'
import ResourceDirectory from './ResourceDirectory'

export default {
  components: { ProjectDetails, ProjectTasks, ResourceDirectory },
  data () {
    return {
      isLoading: true,
      projectId: this.$route.query.id,
      project: null
    }
  },
  mounted () {
    setTimeout(this.getProject, 2000)
    // this.getProject()
  },
  methods: {
    async getProject () {
      this.project = null
      this.isLoading = true
      try {
        const response = await this.$axios.get(`${process.env.BASE_API_URL}/projects/${this.projectId}`)
        this.project = response.data
      } catch (error) {
        this.project = null
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
<style scoped>
.hover-underline > a {
  color: inherit;
  text-decoration: none !important;
}
.hover-underline > a:hover {
  text-decoration: underline !important;
}
</style>
