export const state = () => ({
  isVerified: true,
  wasInformed: false
})

export const mutations = {
  updateVerification (state, verified) {
    state.isVerified = verified
  },
  updateInform (state, inform) {
    state.wasInformed = inform
  }
}
