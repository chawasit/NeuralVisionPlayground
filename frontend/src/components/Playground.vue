<template>
  <div>
    <b-card title="Network Configuration">
      <convolution-network />

      <training-parameter/>

      <div class="mt-3">
        <b-button-group>
          <b-button variant="primary" @click="startTrain" :disabled="disable_form">Train</b-button>
          <b-button variant="danger" @click="reset" :disabled="disable_form">Reset</b-button>
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
    disable_form: state => state.configuration.state != 'new'
  }),
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

