<template>
  <ApolloQuery
    :query="query"
    :variables="queryVariables"
    @result="initItems"
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
        <v-data-table
          :headers="TABLE_HEADERS[resourceType]"
          :items="computedItems"
          :search="search"
          item-key="id"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-container class="py-0" fluid>
              <v-row>
                <v-col class="d-flex align-center">
                  <h1 class="title pt-3 px-3">{{ listingHeader }}</h1>
                </v-col>
                <v-col v-if="resourceType === 'staffs'" class="d-flex justify-end align-center">
                  <v-switch
                    v-model="staffArchive"
                    class="pr-2"
                    label="See Archived"
                  />
                </v-col>
                <v-col v-if="resourceType === 'events'" class="d-flex justify-end align-center">
                  <AddResourceModal :resourceType="resourceType" />
                </v-col>
              </v-row>
              <v-row v-if="resourceType === 'staffs'">
                <v-col>
                  <v-tabs>
                    <v-tab
                      v-for="role in ROLE_OPTIONS"
                      :key="role.value"
                      @click="staffRoleFilter = role.value"
                    >
                      {{ role.label }}
                    </v-tab>
                  </v-tabs>
                </v-col>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="search"
                  label="Search"
                  append-icon="mdi-magnify"
                  solo
                  dense
                  class="mx-3"
                />
              </v-row>
            </v-container>
          </template>

          <!-- Staff/Volunteer Column -->
          <template v-if="resourceType === 'staffs' || resourceType === 'volunteers'" v-slot:[`item.is_speech_therapist`]="{ item }">
            <v-chip v-if="item.is_speech_therapist" color="success">Yes</v-chip>
            <v-chip v-else color="error">No</v-chip>
          </template>

          <template v-slot:[`item.projects_in`]="{ item }">
            {{ item.projects_in.map(project => project.project.title).toString().replace(',', ', ') }}
          </template>

          <!-- Volunteer Specific Columns -->
          <template v-slot:[`item.status`]="{ item }">
            <VolunteerStatusChip :value="item.status" />
          </template>

          <template v-slot:[`item.project_vols`]="{ item }">
            {{ item.project_vols.map(project_vols => project_vols.project.title).toString().replace(',', ', ') }}
          </template>

          <!-- PWA Specific Columns -->
          <template v-slot:[`item.comm_diff`]="{ item }">
            {{ item.comm_diff.map(item => item.difficulty).toString().replaceAll(',', ', ') }}
          </template>

          <template v-slot:[`item.projects`]="{ item }">
            {{ item.projects.map(project => project.project.title).toString().replace(',', ', ') }}
          </template>

          <template v-slot:[`item.languages`]="{ item }">
            {{ item.languages.map(item => item.language).toString().replaceAll(',', ', ') }}
          </template>

          <template v-slot:[`item.nok`]="{ item }">
            {{ item.nok[0] ? item.nok[0].name : '' }}
          </template>

          <template v-slot:[`item.contact_status`]="{ item }">
            <ContactStatusChip :value="item.contact_status" />
          </template>

          <!-- Project Specific Columns -->
          <template v-slot:[`item.staffs`]="{ item }">
            {{ item.staffs.map(item => item.staff.name).toString().replaceAll(',', ', ') }}
          </template>

          <template v-slot:[`item.is_recurring`]="{ item }">
            <IsRecurringChip :value="item.is_recurring" />
          </template>

          <!-- Event Specific Columns -->
          <template v-slot:[`item.event_time`]="{ item }">
            {{ item.start_time.slice(0,5) }} - {{ item.end_time.slice(0,5) }}
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <EditResourceModal v-if="editPermission" :resourceType="resourceType" :resource="item" :text="false" />
            <v-btn v-if="resourceType === 'events'" :to="`/projects?id=${item.project_id}&tab=2&event=${item.id}`" icon>
              <v-icon large>
                mdi-chevron-right
              </v-icon>
            </v-btn>
            <v-btn v-else :to="`/${resourceType}?id=${item.id}`" icon>
              <v-icon large>
                mdi-chevron-right
              </v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </div>

    </template>
  </ApolloQuery>
</template>

<script>
import { LIST_QUERY_PATHS, TABLE_HEADERS, ROLE_OPTIONS, EDIT_RESOURCE_PERMISSIONS } from '../../assets/data'
import EditResourceModal from './../modals/EditResourceModal'
import VolunteerStatusChip from './../common/components/VolunteerStatusChip'
import ContactStatusChip from './../common/components/ContactStatusChip'

export default {
  components: { EditResourceModal, VolunteerStatusChip, ContactStatusChip },
  props: {
    resourceType: {
      type: String,
      default: null
    },
    eventParams: {
      type: Object,
      default: null
    }
  },

  data () {
    return {
      LIST_QUERY_PATHS,
      TABLE_HEADERS,
      ROLE_OPTIONS,
      EDIT_RESOURCE_PERMISSIONS,
      staffRoleFilter: 'core_team',
      search: '',
      staffArchive: false,
      items: [],
      hiddenItems: []
    }
  },

  computed: {
    query () {
      return LIST_QUERY_PATHS[this.resourceType]
    },
    queryVariables () {
      let variables = {}
      if (this.resourceType === 'staffs') {
        variables.isCoreTeam = this.$auth.user['custom:role'] === 'core_team'
      }
      if (this.resourceType === 'events') {
        variables = { ...variables, ...this.eventParams }
      }
      return variables
    },
    listingHeader () {
      let type = this.resourceType.charAt(0).toUpperCase() + this.resourceType.slice(1)
      switch (this.resourceType) {
        case 'pwas':
          type = 'PWAs'
          break
      }
      const header = `Manage ${type}`
      return header
    },
    editPermission () {
      return this.EDIT_RESOURCE_PERMISSIONS[this.resourceType].includes(this.$auth.user['custom:role'])
    },
    computedItems () {
      if (this.resourceType === 'staffs') {
        if (this.staffArchive) {
          return this.items.filter(item => item.role_description.role === this.staffRoleFilter && !item.is_active)
        } return this.items.filter(item => item.role_description.role === this.staffRoleFilter && item.is_active)
      } return this.items
    }
  },

  methods: {
    initItems (result) {
      this.items = result.data[this.resourceType]
    }
  }
}
</script>
