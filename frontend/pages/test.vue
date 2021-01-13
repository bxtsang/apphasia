<template>
  <div>
    <div v-if="!characters">Is Loading</div>
    <li v-else v-for="char in characters.results" :key="char.id">
      {{ char.name }}
    </li>
    <h3 v-if="character">{{ character.name }}</h3>
  </div>
</template>
<script>
import gql from 'graphql-tag'

export default {
  apollo: {
    characters: gql`
    query getCharacters {
        characters {
          results {
            id
            name
          }
        }
    }`,
    character: gql`
    query getCharacter {
      character(id: "${3}") {
        id
        name
      }
    }`
  },
  data () {
    return {
      someId: 3
    }
  }
}
</script>
