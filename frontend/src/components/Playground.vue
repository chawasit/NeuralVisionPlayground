<template>
  <div>
    <b-container>
      <h1>MNIST Playground</h1>
      <p>
        เครื่องมือทดลองการสร้างโมเดลสำหรับการจำแนกตัวเลขจากลายมือ สามารถปรับโครงข่ายประสาทเทียม และตัวแปรต่าง ๆ ในการฝึกสอนได้
      </p>
    </b-container>

    <b-card title="Network Configuration" class="mt-4">
      <p class="card-text">
        กำหนดชั้นต่าง ๆ สำหรับการทำ convolution และ pooling
      </p>

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
          <b-button variant="outline-primary" @click="edit" :disabled="training" v-if="trained">Edit Model</b-button>
          <b-button variant="outline-danger" @click="reset" :disabled="training">Reset Model</b-button>
        </b-button-group>
      </div>
    </b-card>

    <b-card class="mt-4" title="Training Progress" v-if="training">
      <b-progress :value="current_epoch" :max="epoch" show-value animated></b-progress>
    </b-card>

    <b-card class="mt-4" title="Average Accuracy" v-if="accuracy.length>0" @focus="accuracy.length>0">
      <line-chart :height="300" :chart-data="accuracyData"/>
    </b-card>

    <b-card class="mt-4" title="Input Image" v-if="trained">
      <p class="card-text">
        หลังจากที่ฝึกสอนโครงข่ายประสาทเทียมเสร็จแล้ว ในส่วนนี่จะทดการทดลองใช้งานโครงข่ายประสาทเทียมโดยการวาดตัวเลข หรือสุ่มจากข้อมูลตั้งต้น
      </p>

      <b-row>
        <b-col>
          <h5>วาดตัวเลข</h5>
          <black-paper @stopdrawing="runWithImage" :disabled="waitResult"/>
        </b-col>
        <b-col>
          <h5>สุ่มตัวเลข</h5>
          <b-btn-group v-b-tooltip.hover title="สุ่มรูปตัวเลขจากทั้งหมด หรือสุ่มตามเลขที่กำหนด">
          <b-button variant="primary" :disabled="waitResult" @click="run(-1)" >Random</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(0)" >0</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(1)" >1</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(2)" >2</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(3)" >3</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(4)" >4</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(5)" >5</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(6)" >6</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(7)" >7</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(8)" >8</b-button>
          <b-button variant="outline-primary" :disabled="waitResult" @click="run(9)" >9</b-button>
          </b-btn-group>
        </b-col>
      </b-row>
    </b-card>

    <b-card class="mt-4" title="Reaction Inside Network" v-if="waitResult">
      <b-progress :value="100" variant="primary" striped animated class="mb-2"></b-progress>
    </b-card>

    <b-card class="mt-4" title="Reaction Inside Network" v-if="result && trained && !waitResult">
      <b-card class="mt-4" title="Input Image" v-if="trained">
        <b-img :src="result.input_image" />
      </b-card>

      <b-card v-for="{config, images, index} in result.convolution" :key="index">
        <h5>{{ config.type }} layer, kernel size: {{ config.kernel }} {{ config.type === 'convolution' ? `, nodes: ${config.nodes}`: '' }}</h5>
        <b-row >
          <b-col v-for="(image, index) in images" :key="`${config}-${index}`">
            <b-img :src="image" />
          </b-col>
        </b-row>
      </b-card>

      <b-card title="Flatten layer" v-if="trained">
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
    showDismissibleAlert: false,
    waitResult: false
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
      this.waitResult = true
    },
    runWithImage(image) {
      this.$socket.emit('runWithImage', image)
      this.waitResult = true
    }
  },
  watch: {
    error () {
      console.log('Error change')
      this.showDismissibleAlert = true
      this.waitResult = false
    },
    result () {
      this.waitResult = false
    }
  }
}
</script>

