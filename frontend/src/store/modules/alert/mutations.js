
export default {
    hideAlert: (state) => state.alert.display = "none",
    alertSuccess: (state, data) => {
        state.alert.type = "alert alert-success"
        state.alert.img = data.img
        state.alert.msg = data.msg
        state.alert.code = data.code
        state.alert.display = "block"

    },
    alertWarning: (state, data) => {
        // state.alert.type = "alert alert-warning"
        // state.alert.msg = data.msg
        // state.alert.display = "block"
    },
    alertError: (state, data) => {
        state.alert.type = "alert alert-danger"
        state.alert.msg = data.msg
        state.alert.display = "block"
    },
    modalWarning: (state, data) => {

        state.modal.type = "alert alert-warning"
        state.modal.img = data.img
        state.modal.msg = data.msg
        state.modal.code = data.code
        state.modal.display = !state.modal.display
    },
    modalError: (state, data) => {
        state.modal.type = "alert alert-danger"
        state.modal.img = data.img
        state.modal.msg = data.msg
        state.modal.code = data.code
        state.modal.display = !state.modal.display
    },
    resetAlert:(state) => {
        state.alert.type = null
        state.alert.msg = ""
        state.alert.display = "none"
    },
    resetModal:(state) => {
        state.modal.type = null
        state.modal.msg = ""
        state.modal.code = ""
        state.modal.display = false
        state.modal.img = false
    }
}

