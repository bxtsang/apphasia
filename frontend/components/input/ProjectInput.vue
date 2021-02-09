<template>
  <v-select
    v-model="data"
    :items="projects"
    label="Projects Involved"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="disabled"
    multiple
  />
</template>

<script>
import gql from 'graphql-tag'
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'ProjectInput',

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
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      INPUT_VALIDATION,
      validation: [...(this.required ? [INPUT_VALIDATION.project_interest.required] : [])]
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    },
    value: {
      handler (newValue, oldValue) {
        this.data = this.value
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
      },
      update: data => data.projects.map((item) => {
        return { value: item.id, text: item.title }
      })
    }
  }
}

</script>
