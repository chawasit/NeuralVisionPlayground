<template>
  <div>
    <b-card title="Network Configuration">
      <convolution-network />
      
      <b-alert variant="danger"
             dismissible
             :show="showDismissibleAlert"
             @dismissed="showDismissibleAlert=false">
        {{ error }}
      </b-alert>
      
      <training-parameter/>

      <div class="mt-3">
        <b-button-group>
          <b-button variant="outline-primary" @click="startTrain" :disabled="training" v-if="!trained">Train</b-button>
          <b-button variant="outline-primary" @click="edit" :disabled="training" v-if="trained">Edit</b-button>
          <b-button variant="outline-danger" @click="reset" :disabled="training">Reset</b-button>
        </b-button-group>
      </div>
    </b-card>

    <b-card class="mt-4" title="Training" v-if="training">
      <b-progress :value="current_epoch" :max="epoch" show-value animated></b-progress>
    </b-card>

    <b-card class="mt-4" title="Train Accuracy" v-if="accuracy.length>0" @focus="accuracy.length>0">
      <line-chart :height="300" :chart-data="accuracyData"/>
    </b-card>

    <b-card class="mt-4" title="Input Selector" v-if="trained">
      <b-row>
        <b-col>
          <black-paper @stopdrawing="runWithImage" v-b-tooltip.hover title="วาดตัวเลข"/>
        </b-col>
        <b-col>
          <b-btn-group v-b-tooltip.hover title="สุ่มรูปตัวเลขจากทั้งหมด หรือสุ่มตามเลขที่กำหนด">
          <b-button variant="primary" @click="run(-1)" >Random</b-button>
          <b-button variant="outline-primary" @click="run(0)" >0</b-button>
          <b-button variant="outline-primary" @click="run(1)" >1</b-button>
          <b-button variant="outline-primary" @click="run(2)" >2</b-button>
          <b-button variant="outline-primary" @click="run(3)" >3</b-button>
          <b-button variant="outline-primary" @click="run(4)" >4</b-button>
          <b-button variant="outline-primary" @click="run(5)" >5</b-button>
          <b-button variant="outline-primary" @click="run(6)" >6</b-button>
          <b-button variant="outline-primary" @click="run(7)" >7</b-button>
          <b-button variant="outline-primary" @click="run(8)" >8</b-button>
          <b-button variant="outline-primary" @click="run(9)" >9</b-button>
          </b-btn-group>
        </b-col>
      </b-row>
    </b-card>

    <b-card class="mt-4" title="Reaction Inside Layer" v-if="result && trained">
      <b-card class="mt-4" title="Input Image" v-if="trained">
        <b-img :src="result.input_image" />
      </b-card>

      <b-card v-for="{config, images, index} in result.convolution" :key="index">
        <h5>{{ config.type }} layer, kernel size: {{ config.kernel }} {{ config.type === 'convolution' ? `, nodes: ${config.nodes}`: '' }}</h5>
        <b-row >
          <b-col v-for="image in images" :key="image">
            <b-img :src="image" />
          </b-col>
        </b-row>
      </b-card>

      <b-card class="mt-4" title="flatten layer" v-if="trained">
        <b-img :src="result.flatten" />
      </b-card>
      
      <b-card title="Softmax Layer (Prediction)">
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
  data: () => ({
    showDismissibleAlert: false
  }),
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
          label: 'Probability',
          backgroundColor: '#007bff',
          data: state.result.predict
        }
      ]
    }),
    accuracyData: state => ({
      labels: Array(state.train.accuracy.length).fill().map((_, idx) => idx * 10),
      datasets: [
        {
          label: 'Accuracy over epoch',
          backgroundColor: '#007bff',
          data: state.train.accuracy
        }
      ]
    }),
    error: state => state.error
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
    run(id) {
      this.$socket.emit('runRandom', id)
    },
    runWithImage(image) {
      this.$socket.emit('runWithImage', image)
    }
  },
  watch: {
    error () {
      console.log('Error change')
      this.showDismissibleAlert = true
    }
  }
}
</script>

