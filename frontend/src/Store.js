import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        connect: false,
        disableForm: false,
        configuration: null,
        options: null,
        train: { epoch: 0, accuracy: [] },
        result: null,
        error: ""
    },
    mutations:{
        SOCKET_CONNECT: (state) => {
            state.connect = true;
            console.log("Socket Connected")
        },
        SOCKET_DISCONNECT: (state) => {
            state.connect = false;
            console.log("Socket Disconnected")
        },
        SOCKET_STATE: (state,  data) => {
            state.configuration = data[0]
            state.disableForm = state.configuration.state != 'new'
        },
        SOCKET_TRAIN_STATE: (state,  data) => {
            state.train = data[0]
            console.log(state.train)
        },
        SOCKET_RESULT: (state,  data) => {
            state.result = data[0]
            console.log(state.result)
        },
        SOCKET_ERROR: (state, data) => {
            state.error = data[0]
            console.log(state.error)
        }
    },
    actions: {
        
    }
})