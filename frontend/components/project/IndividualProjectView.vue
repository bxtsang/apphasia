<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3" max-width="1600">
        <ApolloQuery
          :query="require('./../../graphql/project/GetSingleProject.graphql')"
          :variables="{ id: projectId }"
        >
          <template v-slot="{ result: { error, data }, isLoading }">
            <div v-if="isLoading" class="d-flex justify-center">
              <v-progress-circular
                :size="50"
                color="primary"
                indeterminate
              />
            </div>

            <!-- Error -->
            <div v-else-if="error">
              An error occurred
            </div>

            <div v-else-if="data && data.projects_by_pk">
              <v-container class="pa-0 ma-0" fluid>
                <v-row>
                  <v-col>
                    <h1 class="title hover-underline">
                      <NuxtLink to="/projects">
                        Projects
                      </NuxtLink> / {{ data.projects_by_pk.title }}
                    </h1>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-tabs  v-model="selectedTab">
                      <v-tab
                        v-for="(tab, index) in tabs"
                        :key="index"
                        @click="$router.push({query: {id: projectId, tab: index}})"
                      >
                        {{ tab }}
                      </v-tab>
                    </v-tabs>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-tabs-items v-model="selectedTab">
                      <!-- Project Details -->
                      <v-tab-item :key="0" transition="fade">
                        <ProjectDetails :project="data.projects_by_pk" :resource-type="resourceType" />
                      </v-tab-item>

                      <!-- Project Resources -->
                      <v-tab-item :key="1" transition="fade">
                        <ResourceDirectory :project="data.projects_by_pk" />
                      </v-tab-item>

                      <!-- Project Events -->
                      <v-tab-item :key="2" transition="fade" >
                        <EventsView :project="data.projects_by_pk" />
                      </v-tab-item>
                    </v-tabs-items>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </template>
        </ApolloQuery>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>

export default {
  props: {
    resourceType: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      projectId: this.$route.query.id,
      selectedTab: this.$route.query.tab ? Number(this.$route.query.tab) : 0,
      tabs: [
        'Details',
        'Resources',
        'Events'
      ]
    }
  }
}
</script>
<style scoped>
.fade-enter-active {
  transition: opacity .3s ease;
  transition-delay: .3s;
}
.fade-leave-active {
  transition: opacity .3s ease;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
