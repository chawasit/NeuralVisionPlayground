import { Bar } from 'vue-chartjs'

export default {
  name: 'BarChart',
  extends: Bar,
  props: ['data'],
  mounted () {
    this.renderChart(this.data, {responsive: true, maintainAspectRatio: false})
  }
}