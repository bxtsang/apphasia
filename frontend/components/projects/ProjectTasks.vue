<template>
  <v-card class="px-6 py-3" height="100%" style="max-height:500px">
    <v-row>
      <v-col>
        <span class="section-title">Project Tasks</span>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary">
          <v-icon left>
            mdi-plus
          </v-icon>
          Add
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-if="isLoading" class="d-flex justify-center">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        />
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
export default {
  data () {
    return {
      isLoading: true,
      projectId: this.$route.query.id,
      tasks: []
    }
  },
  mounted () {
    setTimeout(this.getProjectTasks, 2000)
    // this.getProjectTasks()
  },
  methods: {
    async getProjectTasks () {
      this.tasks = []
      this.isLoading = true
      try {
        const response = await this.$axios.get(`${process.env.BASE_API_URL}/tasks/${this.projectId}`)
        this.tasks = response.data.tasks
      } catch (error) {
        this.tasks = []
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
