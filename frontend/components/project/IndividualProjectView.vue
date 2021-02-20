<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <ApolloQuery
          :query="require('./../../graphql/project/GetSingleProject.graphql')"
          :variables="{ id: projectId }"
        >
          <template v-slot="{ result: { error, data }, isLoading }">
            <div v-if="isLoading" class="d-flex justify-center">
              <v-progress-circular
                :size="50"
                color = "primary"
                indeterminate
              />
            </div>

            <!-- Error -->
            <div v-else-if="error">
              An error occurred
            </div>

            <div v-else-if="data && data.projects_by_pk">
              <v-container class="pa-0 ma-0">
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
                    <v-tabs>
                      <v-tab
                        v-for="(tab, index) in tabs"
                        :key="tab"
                        @click="selectedTab = index"
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
                        <ProjectDetails :project="data.projects_by_pk" :resourceType="resourceType" />
                      </v-tab-item>

                      <!-- Project Resources -->
                      <v-tab-item :key="1" transition="fade">
                        <ResourceDirectory />
                      </v-tab-item>

                      <!-- Project Events -->
                      <v-tab-item :key="2" transition="fade">

                      </v-tab-item>
                    </v-tabs-items>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </template>
        </ApolloQuery>
        <!--
        <v-row>
          <v-col lg="6" md="6" sm="12">
            <ProjectDetails :isLoading="isLoading" :project="project" />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <ResourceDirectory />
          </v-col>
        </v-row> -->
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
      selectedTab: 0,
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
.hover-underline > a {
  color: inherit;
  text-decoration: none !important;
}
.hover-underline > a:hover {
  text-decoration: underline !important;
}
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
