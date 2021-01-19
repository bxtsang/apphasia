export default function ({ $auth, redirect, store }) {
  if (!store.state.email_verified.isVerified && !store.state.email_verified.wasInformed) {
    store.commit('email_verified/updateInform', true)
    redirect('/verifyEmail')
  }
}
