<template>
    <v-autocomplete
    v-model="data"
    :items="colors"
    chips
    :label="label"
    item-text="value"
    item-value="value"
    :rules="validation"
  >
    <template v-slot:selection="data">
      <v-chip
        v-bind="data.attrs"
        :input-value="data.item.value"
        :color="data.item.value"
        dark
      >
        <v-avatar :color="data.item.value" size="35" left />
        {{ data.item.value }}
      </v-chip>
    </template>
    <template v-slot:item="data">
      <template>
        <v-avatar :color="data.item.value" size="35" left class="mr-3"/>
        <v-list-item-content>
          <v-list-item-title>{{ data.item.value }}</v-list-item-title>
        </v-list-item-content>
      </template>
    </template>
  </v-autocomplete>
</template>
<script>
export default {
  data () {
    return {
      data: this.value,
      validation: [v => !!v || 'Color is Required'],
      colors: [
        { value: 'red' },
        { value: 'pink' },
        { value: 'purple' },
        { value: 'deep-purple' },
        { value: 'indigo' },
        { value: 'blue' },
        { value: 'light-blue' },
        { value: 'cyan' },
        { value: 'teal' },
        { value: 'green' },
        { value: 'light-green' },
        { value: 'lime' },
        { value: 'yellow' },
        { value: 'amber' },
        { value: 'orange' },
        { value: 'deep-orange' },
        { value: 'brown' },
        { value: 'blue-grey' }
      ]
    }
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: 'Project Color'
    },
    readonly: {
      type: Boolean,
      default: false
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
  }
}
</script>
