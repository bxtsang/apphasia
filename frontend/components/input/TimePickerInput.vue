<template>
  <v-row no-gutters>
    <v-col cols="4" class="d-flex justify-start align-center">
      <v-subheader class="pa-0">{{ label }}</v-subheader>
    </v-col>
    <v-col cols="4">
      <v-select
        :rules="validation"
        ref="hourInput"
        v-model="data"
        :items="hourItems"
        label="Hour"/>
    </v-col>
    <v-col cols="4">
      <v-select
      v-model="data2"
      :rules="validation"
      ref="minuteInput"
      :items="minuteItems"
      label="Minute"/>
    </v-col>
  </v-row>
</template>
<script>
export default {
  props: {
    value: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Field'
    }
  },
  data () {
    return {
      data: this.value ? this.value.split(':')[0] : '',
      data2: this.value ? this.value.split(':')[1] : '',
      hourItems: Array.from({ length: 24 }, (v, k) => `${k}`.length === 1 ? `0${k}` : `${k}`),
      minuteItems: Array.from({ length: 13 }, (v, k) => `${k * 5}`.length === 1 ? `0${k * 5}` : `${k * 5}`),
      validation: [v => !!v || 'Required']
    }
  },
  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        if (this.minuteItems.includes(this.data2)) {
          this.$emit('input', `${newValue}:${this.data2}`)
        }
      }
    },
    data2: {
      immediate: true,
      handler (newValue, oldValue) {
        if (this.hourItems.includes(this.data)) {
          this.$emit('input', `${this.data}:${newValue}`)
        }
      }
    },
    value: {
      immediate: true,
      handler (newValue, oldValue) {
        if (this.value) {
          this.data = this.value.split(':')[0].length === 1 ? `0${this.value.split(':')[0]}` : this.value.split(':')[0]
          console.log(this.data)
          this.data2 = this.value.split(':')[1]
        }
      }
    }
  }
}
</script>
<style scoped>
.custom-wrapper {
  display: flex;
}
</style>
