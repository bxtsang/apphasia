<template>
  <div>
    <v-row>
      <v-col>
        <v-btn color="primary">
          Add New Project
        </v-btn>
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
              ></v-progress-circular>
            </v-col>
            <v-col v-else v-for="(project, index) in projects" :key="index" cols="6">
              <Project :project="project"></Project>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import Project from '../components/projects/Project.vue'

export default {
  components: { Project },
  data () {
    return {
      isLoading: true,
      projects: []
    }
  },
  mounted () {
    this.getProjects()
  },
  methods: {
    getProjects () {
      this.isLoading = true
      this.projects = [
        { id: 'uid1', name: 'Chit-Chat', task: 2 },
        { id: 'uid2', name: 'Aphasia Choir', task: 3 }
      ]
      this.isLoading = false
    }
  }
}
</script>
