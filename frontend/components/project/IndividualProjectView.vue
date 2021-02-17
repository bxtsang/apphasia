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
                  <v-col>
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
                    <transition-group name="fade" mode="out-in">
                      <div key="0" v-if="selectedTab == 0">Slide 1</div>
                      <div key="1" v-else-if="selectedTab == 1">Slide 2</div>
                      <div key="2" v-else>Slide 3</div>
                    </transition-group>
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
.fade-enter-active, .fade-leave-active {
  transition: opacity .3s ease;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
