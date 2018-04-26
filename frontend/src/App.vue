<template>
  <div id="app">
    <vue-headful title="Neural Vision Playground" />
    <Navbar/>
    
    <b-container class="my-4">
      <b-alert variant="danger"
             dismissible
             :show="showDismissibleAlert"
             @dismissed="showDismissibleAlert=false">
        {{ error }}
      </b-alert>

      <server-disconnected v-if="!connect"/>

      <playground v-if="connect" />
    </b-container>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import ServerDisconnected from './components/ServerDisconnected.vue'
import Playground from './components/Playground.vue'
import { mapState } from 'vuex'
import Store from './Store'

export default {
  name: 'app',
  store: Store,
  data: () => ({
    showDismissibleAlert: false
  }),
  computed: mapState([
    'connect',
    'error'
  ]),
  components: {
    Navbar,
    ServerDisconnected,
    Playground
  },
  watch: {
    error () {
      console.log('Error change')
      this.showDismissibleAlert = true
    }
  }
}
</script>
