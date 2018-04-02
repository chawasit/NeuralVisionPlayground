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

    <b-card class="mt-4" title="Train Accuracy" v-if="accuracy.length>0">
      <line-chart :height="300" :chart-data="accuracyData"/>
    </b-card>

    <b-card class="mt-4" title="Input Selector" v-if="trained">
      <black-paper @stopdrawing="runWithImage" />
      <b-button @click="run" >Random</b-button>
    </b-card>

    <b-card class="mt-4" title="Reaction Inside Layer" v-if="result && trained">
      <b-card v-for="{config, images, index} in result.convolution" :key="index">
        <h5>{{ config.type }} kernel size: {{ config.kernel }} ({{ config.type === 'convolution' ? config.nodes: '' }})</h5>
        <b-row >
          <b-col v-for="image in images" :key="image">
            <b-img :src="image" />
          </b-col>
        </b-row>
      </b-card>
      
      <b-card title="Prediction">
        <bar-chart :height="300" :chart-data="predictData"></bar-chart>
      </b-card>
    </b-card>


  </div>
</template>

<script>
import TrainingParameter from './TrainingParameter.vue'
import ConvolutionNetwork from './ConvolutionNetwork.vue'
import BlackPaper from './BlackPaper.vue'
import BarChart from './BarChart.js'
import LineChart from './LineChart.js'
import { mapState } from 'vuex'

export default {
  name: 'Playground',
  components: {
    BlackPaper,
    ConvolutionNetwork,
    TrainingParameter,
    BarChart,
    LineChart
  },
  computed: mapState({
    trained: state => state.configuration.state == 'trained',
    training: state => state.configuration.state == 'training',
    epoch: state => state.configuration.epoch,
    current_epoch: state => state.train.epoch,
    accuracy: state => state.train.accuracy,
    result: state => state.result,
    predictData: state => ({
      labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
      datasets: [
        {
          label: 'Probability for Number',
          backgroundColor: '#f87979',
          data: state.result.predict.map( n => n * 100)
        }
      ]
    }),
    accuracyData: state => ({
      labels: Array(state.train.accuracy.length).fill().map((_, idx) => idx),
      datasets: [
        {
          label: 'Accuracy over epoch',
          backgroundColor: '#007bff',
          data: state.train.accuracy
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
      this.$socket.emit('runRandom')
    },
    runWithImage(image) {
      this.$socket.emit('runWithImage', image)
    }
  }
}
</script>

