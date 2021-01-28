<template>
  <div>
    <v-checkbox
      v-for="(project, index) in projects"
      :key="project.id"
      v-model="data"
      :rules="validation"
      :label="project.title"
      :value="project.id"
      :hide-details="index !== projects.length - 1"
    />
  </div>
</template>

<script>
import gql from 'graphql-tag'
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'VolunteerProjectInterestInput',

  props: {
    value: {
      type: Array,
      default () {
        return []
      }
    },
    required: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      validation: [INPUT_VALIDATION.project_interest.required]
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    }
  },

  apollo: {
    projects: {
      query () {
        return gql`query getProjects {
          projects {
            id
            title
          }
        }`
      }
    }
  }
}

</script>
