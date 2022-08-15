
export default {
    isAuthenticated: state => state.user,
    isAccess: state => state.accessToken,
    isRefresh: state => state.refreshToken,
}