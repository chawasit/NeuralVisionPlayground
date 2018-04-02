<template>
  <div>
    <b-card title="Network Configuration">
      <convolution-network />

      <training-parameter/>

      <div class="mt-3">
        <b-button-group>
          <b-button variant="primary" @click="startTrain" :disabled="disableForm">Train</b-button>
          <b-button variant="danger" @click="reset" :disabled="disableForm">Reset</b-button>
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
  computed: mapState([
    'disableForm'
  ]),
  methods: {
    startTrain() {
      this.$socket.emit('start_train')
    },
    reset() {
      this.$socket.emit('reset')
    }
  }
}
</script>

