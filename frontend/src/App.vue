<template>
  <div id="app">
    <vue-headful title="Neural Vision Playground" />
    <Navbar @selected="selected" />
    
    <b-container class="my-4" v-show="playground">
      <server-disconnected v-if="!connect"/>

      <playground v-if="connect" />
    </b-container>

    <b-container class="my-4" v-show="!playground">
      <tutorial />
    </b-container>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import ServerDisconnected from './components/ServerDisconnected.vue'
import Playground from './components/Playground.vue'
import Tutorial from './components/Tutorial.vue'
import { mapState } from 'vuex'
import Store from './Store'

export default {
  name: 'app',
  store: Store,
  data: () => ({
    playground: true 
  }),
  computed: mapState([
    'connect',
    'error'
  ]),
  components: {
    Navbar,
    ServerDisconnected,
    Playground,
    Tutorial
  },
  methods: {
    selected (menu) {
      this.playground = menu == 'playground'
    }
  }
}
</script>
