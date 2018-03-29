<template>
  <div id="app">
    <Navbar/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Navbar from './components/Navbar.vue'

export default {
  name: 'app',
  sockets: {
    connect () {
      console.log("Socket connected")
    }
  },
  components: {
    Navbar
  },
}
</script>
