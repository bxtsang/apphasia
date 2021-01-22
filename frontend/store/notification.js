export const state = () => ({
  message: '',
  status: ''
})

export const mutations = {
  newMessage (state, message) {
    state.message = message
  },
  newStatus (state, status) {
    state.status = status
  },
  newNotification (state, data) {
    state.message = data[0]
    state.status = data[1]
  }
}
