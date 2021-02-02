<template>
  <v-select
    v-model="data"
    :items="projects"
    label="Projects Involved"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="true"
    multiple
  />
</template>

<script>
import gql from 'graphql-tag'

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
      type: Boolan,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      validation: []
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
      },
      update: data => data.projects.map((item) => {
        console.log(item)
        return { value: item.id, text: item.title }
      })
    }
  }
}

</script>
