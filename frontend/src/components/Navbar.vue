<template>
  <b-navbar toggleable="md" type="dark" variant="primary">
    <div class="container">
      <b-navbar-brand href="#">Neural Vision Playground</b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav>
          <b-nav-item href="#" @click="select('playground')">Playground</b-nav-item>
          <b-nav-item href="#" @click="select('tutorial')">Tutorial</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </div>
  </b-navbar>
</template>

<script>
export default {
  name: 'Navbar',
  methods: {
    select (t) {
      this.$emit('selected', t)
    }
  }
}
</script>

