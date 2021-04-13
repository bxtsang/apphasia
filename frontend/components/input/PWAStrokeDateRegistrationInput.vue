<template>
  <v-menu
    transition="scale-transition"
    offset-y
    :close-on-content-click="false"
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <div class="d-flex align-center">
        <v-btn
          v-on="on"
          v-bind="attrs"
          fab
          icon
          small
          class="blink-animation mr-3"
        >
          <v-icon>mdi-calendar</v-icon>
        </v-btn>
        <v-text-field
          v-model="month"
          :rules="validationMonth"
          label="Month"
          type="number"
        />
        <div class="px-3">/</div>
        <v-text-field
          v-model="year"
          :rules="validationYear"
          label="Year"
          type="number"
          min='1900'
          :max="new Date().getFullYear()"
        />
      </div>
    </template>
    <v-date-picker
      ref="picker"
      type="month"
      v-model="data"
      :max="new Date().toISOString().substr(0, 10)"
    />
  </v-menu>
</template>

<script>

export default {
  name: 'StrokeDateInput',

  props: {
    value: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    outlined: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      month: '',
      year: '',
      validationMonth: [v => (v > 0 && v < 13) || 'Valid month is required'],
      validationYear: [v => (v > 1900 && v <= new Date().getFullYear()) || 'Valid year is required']
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.month = newValue.split('-')[1]
        this.year = newValue.split('-')[0]
        this.$emit('input', newValue)
      }
    },
    value: {
      handler (newValue, oldValue) {
        this.data = this.value
      }
    },
    month: {
      handler (newValue, oldValue) {
        if (this.year) {
          this.data = `${this.year}-${newValue}`
        }
      }
    },
    year: {
      handler (newValue, oldValue) {
        if (this.month) {
          this.data = `${newValue}-${this.month}`
        }
      }
    }
  }
}

</script>
<style scoped>
.blink-animation {
  animation: 3s infinite blink;
}

@keyframes blink {
  0% {
    background-color: transparent;
  }
  50% {
    background-color: lightgray;
  }
  100% {
    background-color: transparent;
  }
}
</style>
