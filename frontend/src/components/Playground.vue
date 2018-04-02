<template>
  <div>
    <b-card title="Network Configuration">
      <convolution-network />

      <training-parameter/>

      <div class="mt-3">
        <b-button-group>
          <b-button variant="primary" @click="startTrain" :disabled="disable" v-if="!trained">Train</b-button>
          <b-button @click="edit" :disabled="disable" v-if="trained">Edit</b-button>
          <b-button variant="danger" @click="reset" :disabled="disable">Reset</b-button>
        </b-button-group>
      </div>
    </b-card>
  </div>
</template>

<script>
import TrainingParameter from './TrainingParameter.vue'
import ConvolutionNetwork from './ConvolutionNetwork.vue'
import BlackPaper from './BlackPaper.vue'
import { mapState } from 'vuex'

export default {
  name: 'Playground',
  components: {
    BlackPaper,
    ConvolutionNetwork,
    TrainingParameter
  },
  computed: mapState({
    disable: state => state.configuration.state == 'training',
    trained: state => state.configuration.state == 'trained'
  }),
  methods: {
    startTrain() {
      this.$socket.emit('start_train')
    },
    edit() {
      this.$socket.emit('edit')
    },
    reset() {
      this.$socket.emit('reset')
    }
  }
}
</script>

