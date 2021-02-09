<template>
  <div>
    <v-checkbox
      v-for="profession in COMMON_PROFESSIONS"
      :key="profession"
      v-model="data"
      :rules="validation"
      :label="profession"
      :value="profession"
      hide-details
    />
    <div class="d-flex">
      <v-checkbox
        v-model="data"
        :value="othersValue"
        :rules="validation"
        label="Other: "
      />
      <v-text-field
        v-model="othersValue"
      />
    </div>
  </div>
</template>

<script>
import { INPUT_VALIDATION, COMMON_PROFESSIONS } from './../../assets/data'

export default {
  name: 'MultiProfessionInput',

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
      COMMON_PROFESSIONS,
      data: this.value,
      othersEnabled: false,
      othersValue: '',
      validation: [INPUT_VALIDATION.multi_profession.required]
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    },
    othersValue: {
      handler (newValue, oldValue) {
        const oldArray = this.data.filter(item => item !== oldValue)
        this.data = [...oldArray, newValue]
      }
    },
    value: {
      handler (newValue, oldValue) {
        this.data = this.value
      }
    }
  }
}

</script>
