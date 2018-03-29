<template>
  <div id="app">
    <Navbar/>
    <div class="container py-5">
      <server-disconnected v-if="!isConnected"/>
      <tensorflow v-if="isConnected" />
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import ServerDisconnected from './components/ServerDisconnected.vue'
import Tensorflow from './components/Tensorflow.vue'

export default {
  name: 'app',
  data: () => ({
    isConnected: false
  }),
  sockets: {
    connect () {
      this.isConnected = true
      console.log("Socket connected")
    },
    disconnect () {
      this.isConnected = false
      console.log("Socket disconnected")
    }
  },
  components: {
    Navbar,
    ServerDisconnected,
    Tensorflow
  },
}
</script>
