<template>
  <v-select
    v-model="data"
    :items="languages"
    :label="!placeholderOnly ? 'Languages understand and/or speak' : ''"
    :placeholder="placeholderOnly ? 'Select language(s)' : ''"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    multiple
  />
</template>

<script>
import gql from 'graphql-tag'
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'LanguageInput',

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
    placeholderOnly: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      validation: [INPUT_VALIDATION.languages.required]
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
    languages: {
      query () {
        return gql`query getLanguages {
          languages {
            language
            description
          }
        }`
      },
      update: data => data.languages.map((item) => {
        return { value: item.language, text: item.description }
      })
    }
  }
}

</script>
