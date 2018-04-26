<template>
  <b-container>
    <h1>Tutorial</h1>
    <div class="float-right sticky-top pt-4">
      <b-list-group v-b-scrollspy>
        <b-list-group-item href="#item-1">Item 1</b-list-group-item>
        <b-list-group-item href="#item-1-1">Item 4</b-list-group-item>
        <b-list-group-item href="#item-1-2">Item 5</b-list-group-item>
        <b-list-group-item href="#item-2">Item2</b-list-group-item>
        <b-list-group-item href="#item-3">Item 3</b-list-group-item>
      </b-list-group>
    </div>
    <b-row>
      <b-col cols="10">
        <div>
          <h4 id="item-1" style="">Item 1</h4>
          <p>{{ text }}</p>
          <p>{{ text }}</p>
          <h5 id="item-1-1" style="">Item 1-1</h5>
          <p>{{ text }}</p>
          <p>{{ text }}</p>
          <p>{{ text }}</p>
          <h5 id="item-1-2" style="">Item 1-2</h5>
          <p>{{ text }}</p>
          <p>{{ text }}</p>
          <h4 id="item-2" style="">Item 2</h4>
          <p>{{ text }}</p>
          <p>{{ text }}</p>
          <p>{{ text }}</p>
          <h4 id="item-3" style="">Item 3</h4>
          <p>{{ text }}</p>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'Tutorial',
  data: () => ({
    text: `
      Quis magna Lorem anim amet ipsum do mollit sit cillum voluptate ex nulla
        tempor. Laborum consequat non elit enim exercitation cillum aliqua
        consequat id aliqua. Esse ex consectetur mollit voluptate est in duis
        laboris ad sit ipsum anim Lorem. Incididunt veniam velit elit elit veniam
        Lorem aliqua quis ullamco deserunt sit enim elit aliqua esse irure. Laborum
        nisi sit est tempor laborum mollit labore officia laborum excepteur
        commodo non commodo dolor excepteur commodo. Ipsum fugiat ex est consectetur
        ipsum commodo tempor sunt in proident.
    `
  })
}
</script>
