<template>
  <div>
    <b-card title="Network Configuration">
      <convolution-network />

      <training-parameter/>

      <div class="mt-3">
        <b-button-group>
          <b-button variant="primary" @click="startTrain" :disabled="training" v-if="!trained">Train</b-button>
          <b-button @click="edit" :disabled="training" v-if="trained">Edit</b-button>
          <b-button variant="danger" @click="reset" :disabled="training">Reset</b-button>
        </b-button-group>
      </div>
    </b-card>

    <b-card class="mt-4" title="Training" v-if="training">
      <b-progress :value="current_epoch" :max="epoch" show-value animated></b-progress>
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
  data: () => ({
    counter: 360,
    max: 1000
  }),
  computed: mapState({
    trained: state => state.configuration.state == 'trained',
    training: state => state.configuration.state == 'training',
    epoch: state => state.configuration.epoch,
    current_epoch: state => state.train.epoch
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

