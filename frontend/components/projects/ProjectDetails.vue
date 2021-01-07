<template>
  <v-card class="px-6 py-3" height="100%" style="max-height:500px">
    <v-row>
      <v-col>
        <span class="section-title">Project Details</span>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary">
          <v-icon left>
            mdi-pencil
          </v-icon>
          Edit
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
      <v-col v-else>
        <v-text-field :value="project.name" label="Project Name" readonly />
        <v-text-field :value="project.description" label="Project Description" readonly />
        <v-autocomplete
          v-model="assignedMembers"
          :items="project.assigned"
          chips
          label="Project Assignment"
          item-text="name"
          item-value="id"
          multiple
          readonly
        >
          <template v-slot:selection="data">
            <v-chip
              class="my-2"
              v-bind="data.attrs"
              :input-value="data.selected"
            >
              {{ data.item.name }}
            </v-chip>
          </template>
          <template v-slot:item="data">
            <v-list-item-content>
              <v-list-item-title v-text="data.item.name" />
            </v-list-item-content>
          </template>
        </v-autocomplete>
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
export default {
  props: { project: Object, isLoading: Boolean },
  data () {
    return {
      editorOpen: false,
      assignedMembers: []
    }
  },
  watch: {
    project () {
      if (this.project.assigned && this.project.assigned.length > 0) {
        this.assignedMembers = this.project.assigned.map(item => item.id)
      } else {
        this.assignedMembers = []
      }
    }
  }
}
</script>
