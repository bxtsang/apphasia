<template>
  <ApolloQuery
    :query="LIST_QUERY_PATHS['staffVolPWA']"
    :update="queryMutation"
  >
    <template v-slot="{ result: { error, data }, isLoading }">
      <!-- Loading -->
      <div v-if="isLoading" class="d-flex justify-center">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        />
      </div>

      <!-- Error -->
      <div v-else-if="error">An error occurred</div>

      <!-- Result -->
      <div v-else-if="data">
        <v-row>
          <v-col>
            <span class="font-weight-bold">Project Assignment</span>
          </v-col>
        </v-row>
        <v-data-table
          :headers="[{ text: 'id', value: 'id' }]"
          :items="[]"
          item-key="id"
          class="elevation-1"
        >
          <template v-slot:top>
          </template>
        </v-data-table>
        <pre>{{ data }}{{ staffs }}{{ volunteers }}{{ pwas }}</pre>
      </div>

    </template>
  </ApolloQuery>
</template>
<script>
import { LIST_QUERY_PATHS } from './../../../assets/data.js'

export default {
  data () {
    return {
      LIST_QUERY_PATHS,
      data: this.value
    }
  },

  props: {
    value: {
      type: Object,
      default () {
        return {
          pwa_assigned_vols: { data: [] },
          pwa_assigned_staffs: { data: [] }
        }
      }
    },
    staffs: {
      type: Array,
      default () {
        return []
      }
    },
    volunteers: {
      type: Array,
      default () {
        return []
      }
    },
    pwas: {
      type: Array,
      default () {
        return []
      }
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

  methods: {
    queryMutation (data) {
      return data.volunteers
    }
  }
}
</script>
