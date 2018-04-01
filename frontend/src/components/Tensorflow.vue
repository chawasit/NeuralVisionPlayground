<template>
  <div>
    <b-card title="System Configuration">
      <!-- training parameter -->
      <b-form disabled>
        <b-form-row>
          <!-- learning rate selector -->
          <b-col>
            <b-form-group id="learningRateGroupSelector"
                    label="Learning rate:"
                    label-for="learningRateSelector"
                    description="อัตราการเรียนรู้">
              <b-form-select v-model="configuration.learningRate"
                            :options="learningRateOptions"
                            id="learningRateSelector"
                            aria-describedby="learningRateHelper"
                            required
                            disabled>
              </b-form-select>
            </b-form-group>
          </b-col>
          <!-- end learning rate selector -->

          <!-- activation selector -->
          <b-col>
            <b-form-group id="activationGroupSelector"
                    label="Activation:"
                    label-for="activationSelector"
                    description="ฟังก์ชั่นระบบประสาท">
              <b-form-select v-model="configuration.activation"
                            :value="null"
                            :options="activationOptions"
                            id="activationSelector"
                            aria-describedby="activationHelper">
              </b-form-select>
            </b-form-group>
          </b-col>
          <!-- end activation selector -->

          <!-- epoch selector -->
          <b-col>
            <b-form-group id="epochGroupSelector"
                    label="Epoch:"
                    label-for="epochSelector"
                    description="จำนวนรอบในการฝึกสอน">
              <b-form-input v-model="configuration.epoch"
                            id="epochSelector"
                            type="range"
                            min="100"
                            max="3000"
                            step="100">
              </b-form-input>
              <b-form-text>{{ configuration.epoch }}</b-form-text>
            </b-form-group>
          </b-col>
          <!-- end epoch selector -->

          <!-- batch size selector -->
          <b-col>
            <b-form-group id="batchSizeGroupSelector"
                    label="Batch size:"
                    label-for="batchSizeSelector"
                    description="จำนวนข้อมูลในแต่ละรอบการฝึกสอน">
              <b-form-input v-model="configuration.batchSize"
                            id="batchSizeSelector"
                            type="range"
                            min="10"
                            max="200"
                            step="10">
              </b-form-input>
              <b-form-text>{{ configuration.batchSize }}</b-form-text>
            </b-form-group>
          </b-col>
          <!-- end batch size selector -->
        </b-form-row>
      </b-form>
      <!-- end training parameter -->

      <!-- Layer parameter -->
      <b-row>
        <!-- convolution layer -->
        <b-col>
          <b-card title="Convolution & Pooling">
            <b-button href="#" variant="info">add layer</b-button>
          </b-card>
          
        </b-col>
        <!-- end covolution layer -->

        <!-- classification layer -->
        <b-col>
          <b-card title="Fully Connected">
            <b-button href="#" variant="info">add layer</b-button>
          </b-card>
        </b-col>
        <!-- end classification layer -->
      </b-row>
      <!-- end Layer parameter -->

      <div class="mt-3">
        <b-button href="#" variant="primary">Train</b-button>
      </div>
    </b-card>

    <!-- draw image Input -->
    <b-card title="Input" class="mt-4">
      <b-row>
        <b-col>
          <black-paper v-on:stopdrawing="drawingNumber"/>
        </b-col>
        <b-col></b-col>
        <b-col></b-col>
        <b-col></b-col>

      </b-row>
      

    </b-card>
    



    <!-- end draw image input -->
    
  </div>
</template>

<script>
import BlackPaper from './BlackPaper.vue'

export default {
  name: 'Tensorflow',
  data: () => ({
    learningRateOptions: {'0.01': '0.01'
                          ,'0.001': '0.001'
                          ,'0.0001': '0.0001'},
    activationOptions: {'sigmoid': 'Sigmoid'
                        , 'tanh': 'Tanh'
                        , 'relu': 'RELU'
                        , 'linear': 'Linear' },
    configuration: {
      trained: false,
      learningRate: 0.01,
      activation: 'sigmoid',
      epoch: 700,
      batchSize: 100,
      convolutions: [
        { 
          type: 'convolution',
          kernelSize: { height: 5, width: 5 },
          numberOfNodes: 6
        },
        { 
          type: 'pooling',
          kernelSize: { height: 5, width: 5 },
          numberOfNodes: 6
        },
        { 
          type: 'convolution',
          kernelSize: { height: 5, width: 5 },
          numberOfNodes: 6
        }
      ],
      classification: [

      ]
    }
  }),
  methods: {
    drawingNumber (dataURL) {
      console.log(dataURL)
    }
  },
  created () {

  },
  components: {
    BlackPaper
  }
}
</script>

