export const state = () => ({
  expiration: null
})

export const mutations = {
  updateExpiration (state, datetime) {
    state.expiration = datetime
  }
}
