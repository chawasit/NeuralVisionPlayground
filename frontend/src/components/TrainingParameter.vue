<template>
  <b-card title="Training Parameters">
    <p class="card-text">
      ตัวแปรต่าง ๆ ในการฝึกสอนโครงข่ายประสาทเทียม
    </p>

    <!-- training parameter -->
    <b-form class="mt-3">
      <b-form-row>
        <!-- learning rate selector -->
        <b-col>
          <b-form-group id="learningRateGroupSelector"
                  label="Learning rate:"
                  label-for="learningRateSelector"
                  description="อัตราการเรียนรู้">
            <b-form-select :value="learningRate"
                          :options="learningRateOptions"
                          @change="setLearningRate"
                          id="learningRateSelector"
                          aria-describedby="learningRateHelper"
                          :disabled="disableForm">
            </b-form-select>
          </b-form-group>
        </b-col>
        <!-- end learning rate selector -->

        <!-- dropout selector -->
        <b-col>
          <b-form-group id="dropoutGroupSelector"
                  label="Dropout:"
                  label-for="dropoutSelector"
                  description="อัตราการปล่อยวาง">
            <b-form-input :value="dropout"
                          @change="setDropout"
                          id="dropoutSelector"
                          type="number"
                          min="0"
                          max="1"
                          step="0.1"
                          :disabled="disableForm">
            </b-form-input>
          </b-form-group>
        </b-col>
        <!-- end dropout selector -->

        <!-- epoch selector -->
        <b-col>
          <b-form-group id="epochGroupSelector"
                  label="Epoch:"
                  label-for="epochSelector"
                  description="จำนวนรอบในการฝึกสอน">
            <b-form-input :value="epoch"
                          @change="setEpoch"
                          id="epochSelector"
                          type="number"
                          min="100"
                          max="3000"
                          step="100"
                          :disabled="disableForm">
            </b-form-input>
          </b-form-group>
        </b-col>
        <!-- end epoch selector -->

        <!-- batch size selector -->
        <b-col>
          <b-form-group id="batchSizeGroupSelector"
                  label="Batch size:"
                  label-for="batchSizeSelector"
                  description="จำนวนข้อมูลในแต่ละรอบการฝึกสอน">
            <b-form-input :value="batchSize"
                          @change="setBatchSize"
                          id="batchSizeSelector"
                          type="number"
                          min="10"
                          max="200"
                          step="10"
                          :disabled="disableForm">
            </b-form-input>
          </b-form-group>
        </b-col>
        <!-- end batch size selector -->
      </b-form-row>
    </b-form>
    <!-- end training parameter -->
  </b-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'TrainingParameter',
  data: () => ({
    learningRateOptions: [0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003, 0.00001],
  }),
  computed: mapState({
    disableForm: 'disableForm',
    learningRate: state => state.configuration.learning_rate,
    dropout: state => state.configuration.dropout,
    epoch: state => state.configuration.epoch,
    batchSize: state => state.configuration.batch_size,
    convolutionNetwork: state => state.configuration.convolution_network
  }),
  methods: {
    setLearningRate(value) {
      this.$socket.emit('change_learning_rate', value)
    },
    setDropout(value) {
      this.$socket.emit('change_dropout', value)
    },
    setEpoch(value) {
      this.$socket.emit('change_epoch', value)
    },
    setBatchSize(value) {
      this.$socket.emit('change_batch_size', value)
    }
  }
}
</script>

