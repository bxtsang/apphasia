<template>
  <v-card width="100%">
    <v-container fill-height>
      <v-row>
        <v-col class="d-flex justify-center">
          <v-img src="/undraw_approve.svg" max-width="500"/>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="success-text d-flex align-center flex-column">
          <h1 class="pb-6">Yay, you have been registered!</h1>
          <p class="pb-3">Thank you for your interest in being a part of the aphasia movement in Singapore! We will contact you shortly to get to know you better!</p>
          <p>Till then, stay safe and healthy 😊</p>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
<style scoped>
.success-text > h1 {
  font-size: 2.3rem;
  text-align: center;
}
.success-text > p {
  display: block;
  max-width: 850px;
  font-size: 1.5rem;
  text-align: center;
  font-weight: 300;
}
</style>
