<template>
  <div id="app">
    <vue-headful title="Neural Vision Playground" />
    <Navbar/>
    <b-container class="py-4">
      <server-disconnected v-if="!connect"/>
      <tensorflow v-if="connect" />
    </b-container>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import ServerDisconnected from './components/ServerDisconnected.vue'
import Tensorflow from './components/Tensorflow.vue'
import { mapState } from 'vuex'
import Store from './Store'

export default {
  name: 'app',
  store: Store,
  computed: mapState([
    'connect'
  ]),
  components: {
    Navbar,
    ServerDisconnected,
    Tensorflow
  },
}
</script>
