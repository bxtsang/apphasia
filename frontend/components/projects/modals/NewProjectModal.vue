<template>
  <v-dialog
    v-model="isOpen"
    width="600"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on">
        Add New Project
      </v-btn>
    </template>
    <v-card class="pa-8">
      <span class="section-title">New Project</span>
      <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="submitProject">
        <v-text-field
          v-model="projectData.name"
          :rules="nameRules"
          label="Project Name"
          required
        />
        <v-text-field
          v-model="projectData.description"
          :rules="descriptionRules"
          label="Project Description"
          required
        />
        <v-autocomplete
          v-model="assignedMembers"
          :items="assignList"
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
        <v-btn color="primary" class="my-3" type="submit">
          Save
        </v-btn>
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data () {
    return {
      isOpen: false,
      valid: true,
      projectData: {
        name: '',
        description: '',
        assignment: []
      },
      assignList: []
    }
  },
  methods: {
    submitProject () {
      return this.$refs.form.validate()
    }
  }
}
</script>
