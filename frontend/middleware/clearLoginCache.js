export default function ({ $auth, redirect, store, $apolloHelpers }) {
  const user = $auth.user
  if (user) {
    $apolloHelpers.onLogout()
  }
}
