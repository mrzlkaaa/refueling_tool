
export default {
    async resetAlert({commit}){
        commit("resetAlert")
    },
    async resetModal({commit}){
        commit("resetModal")
    },
    hideAlert: async ({commit}, duration) => {
        setTimeout(() => {commit('hideAlert')}, 7000)
    },
    async alertSuccess({commit}, data) {
        commit("alertSuccess", data)
    },
    async alertWarning({commit}, data){
        commit("alertWarning", data)
    },
    async alertError({commit}, data){
        commit("alertError", data)
    },
    async modalWarning({commit}, data){
        commit("modalWarning", data)
    },
    async modalError({commit}, data){
        commit("modalError", data)
    }
}