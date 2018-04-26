import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import vueHeadful from 'vue-headful';
import VueSocketio from 'vue-socket.io';

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Store from './Store.js'

Vue.use(Vuex);
Vue.component('vue-headful', vueHeadful);

Vue.use(VueSocketio, ':5000', Store);
Vue.use(BootstrapVue);

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
