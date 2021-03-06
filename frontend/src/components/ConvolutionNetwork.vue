<template>
  <b-container>
    <b-table :items="layers" :fields="fields" caption-top>
      <template slot="index" slot-scope="data">
        {{ data.index + 1 }}
      </template>
      <template slot="type" slot-scope="data">
        {{ layerTypeOptions[data.value] }}
      </template>
      <template slot="type" slot-scope="data">
        {{ layerTypeOptions[data.value] }}
      </template>
      <template slot="nodes" slot-scope="row">
        {{ row.item.type==='convolution'?row.item.nodes:'' }}
      </template>
      <template slot="action" slot-scope="row">
        <b-button-group size="sm">
          <b-button @click.stop="row.toggleDetails" variant="outline-primary" :disabled="disableForm">
           {{ row.detailsShowing ? 'Done' : 'Edit'}}
          </b-button>
          <b-button variant="outline-info" @click="moveLayer(row.index, -1)" :disabled="disableForm">
            Up
          </b-button>
          <b-button variant="outline-info" @click="moveLayer(row.index, 1)" :disabled="disableForm">
            Down
          </b-button>
          <b-button variant="outline-danger" @click="removeLayer(row.index)" :disabled="disableForm">
            Remove
          </b-button>
        </b-button-group>
      </template>
      <template slot="row-details" slot-scope="row">
        <b-card>
          <b-form-row>
            <!-- learning rate selector -->
            <b-col>
              <b-form-group id="typeGroupSelector"
                      label="Type:"
                      label-for="typeSelector"
                      description="รูปแบบการทำงาน">
                <b-form-select :value="row.item.type"
                              :options="layerTypeOptions"
                              @change="setType($event, row.index)"
                              id="typeSelector"
                              aria-describedby="learningRateHelper"
                              :disabled="disableForm">
                </b-form-select>
              </b-form-group>
            </b-col>
            <!-- end learning rate selector -->

            <!-- dropout selector -->
            <b-col>
              <b-form-group id="kernelGroupSelector"
                      label="Kernel Size:"
                      label-for="kernelSelector"
                      description="ขนาดของหน้าต่าง">
                <b-form-input :value="row.item.kernel"
                              @change="setKernel($event, row.index)"
                              id="kernelSelector"
                              type="number"
                              min="1"
                              max="10"
                              step="1"
                              :disabled="disableForm">
                </b-form-input>
              </b-form-group>
            </b-col>
            <!-- end dropout selector -->

            <!-- epoch selector -->
            <b-col>
              <b-form-group id="nodeGroupSelector"
                      label="Number of Node:"
                      label-for="nodeSelector"
                      description="จำนวนโหนดภายใน"
                      v-show="row.item.type==='convolution'">
                <b-form-input :value="row.item.nodes"
                              @change="setNodes($event, row.index)"
                              id="nodeSelector"
                              type="number"
                              min="1"
                              max="30"
                              step="1"
                              :disabled="disableForm">
                </b-form-input>
              </b-form-group>
            </b-col>
            <!-- end epoch selector -->
          </b-form-row>
        </b-card>
      </template>
    </b-table>
    <b-button size="sm" class="mb-4" variant="outline-primary" @click="addLayer" :disabled="disableForm">Add Layer</b-button>
  </b-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ConvolutionNetwork',
  data: () => ({
    layerTypeOptions: {
      'max_pool': 'max pool',
      'avg_pool': 'average pool',
      'convolution': 'convolution'
    },
    fields: [
      { key: 'index', label: 'Layer no.' },
      { key: 'type', label: 'Type' },
      { key: 'kernel', label: 'Kernel Size' },
      { key: 'nodes', label: 'Number of Node' },
      'action'
    ]
  }),
  computed: mapState({
      disableForm: 'disableForm',
      layers: state => state.configuration.convolution_network,
  }),
  methods: {
    addLayer() {
      this.$socket.emit('add_layer')
    },
    removeLayer(index) {
      this.$socket.emit('remove_layer', index)
    },
    moveLayer(index, level) {
      this.$socket.emit('move_layer', {index: index, level: level})
    },
    setType(value, index) {
      this.$socket.emit('change_layer_type', {index: index, value: value})
    },
    setKernel(value, index) {
      this.$socket.emit('change_layer_kernel', {index: index, value: value})
    },
    setNodes(value, index) {
      this.$socket.emit('change_layer_nodes', {index: index, value: value})
    }
  }
}
</script>
