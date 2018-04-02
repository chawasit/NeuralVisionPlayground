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

    <b-card class="mt-4" title="Input Selector" v-if="trained">
      <b-button @click="run" >Run</b-button>
    </b-card>

    <b-card class="mt-4" title="Reaction Inside Layer" v-if="result">
      <b-card v-for="{config, images, index} in result.convolution" :key="index">
        <h5>{{ config.type }} kernel size: {{ config.kernel }} ({{ config.type === 'convolution' ? config.nodes: '' }})</h5>
        <b-row >
          <b-col v-for="image in images" :key="image">
            <b-img :src="image" />
          </b-col>
        </b-row>
      </b-card>
      
      <b-card title="Prediction">
        <bar-chart :data="predictData"></bar-chart>
      </b-card>
    </b-card>


  </div>
</template>

<script>
import TrainingParameter from './TrainingParameter.vue'
import ConvolutionNetwork from './ConvolutionNetwork.vue'
import BlackPaper from './BlackPaper.vue'
import BarChart from './BarChart.js'
import { mapState } from 'vuex'

export default {
  name: 'Playground',
  components: {
    BlackPaper,
    ConvolutionNetwork,
    TrainingParameter,
    BarChart
  },
  computed: mapState({
    trained: state => state.configuration.state == 'trained',
    training: state => state.configuration.state == 'training',
    epoch: state => state.configuration.epoch,
    current_epoch: state => state.train.epoch,
    result: state => state.result,
    predictData: state => ({
        labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        datasets: [
          {
            label: 'Number',
            backgroundColor: '#f87979',
            data: state.result.predict.map( n => n * 100)
          }
        ]
      })
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
    },
    run() {
      this.$socket.emit('run', 'data')
    }
  }
}
</script>

