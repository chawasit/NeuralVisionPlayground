<template>
  <b-container>
    <b-row>
      <canvas ref="canvas"
                @mousedown="mousedown"
                @mousemove="mousemove"
                @mouseup="mouseup"
                @mouseout="mouseup"
                width="300px"
                height="300px"
                style="background: #000; width: 300px; height: 300px"/>
    </b-row>
    <b-row class="mt-2">
      <b-btn-group>
      <b-button variant="outline-primary" :disabled="disabled" @click="send">Send</b-button>
      <b-button variant="outline-danger" :disabled="disabled" @click="reset">Reset Canvas</b-button>
      </b-btn-group>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'BlackPaper',
  data: () => ({
    draw: {
      clickX: [],
      clickY: [],
      dragging: [],
      isPainting: false,
      lastData: ''
    }
  }),
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    addClick (x, y, dragging) {
      this.draw.clickX.push(x)
      this.draw.clickY.push(y)
      this.draw.dragging.push(dragging)
    },
    redraw () {
      const canvas =  this.$refs.canvas
      const context = canvas.getContext("2d")
      context.fillStyle = "#000"
      context.fillRect(0,0,context.canvas.width, context.canvas.height)
      context.fillStyle = "#fff"
      context.strokeStyle = "#fff"
      context.lineJoin = "round"
      context.lineWidth = 24
      
      var clickX = this.draw.clickX
      var clickY = this.draw.clickY
      var clickDrag = this.draw.dragging
      for(var i=0; i < clickX.length; i++) {		
        context.beginPath();
        if(clickDrag[i]){
          context.moveTo(clickX[i-1], clickY[i-1]);
        }else{
          context.moveTo(clickX[i]-1, clickY[i]);
        }
        context.lineTo(clickX[i], clickY[i]);
        context.closePath();
        context.stroke();
      }
    },
    resetCanvas () {
      this.draw.clickX = []
      this.draw.clickY = []
      this.draw.dragging = []
    },
    mousedown (event) {
      this.draw.isPainting = true;
      if (this.draw.isPainting && !this.disabled) {
        this.addClick(
          event.offsetX,
          event.offsetY,
        )
        this.redraw()
      }
    },
    mouseup () {
      this.draw.isPainting = false
    },
    mousemove (event) {
      if (this.draw.isPainting && !this.disabled) {
        this.addClick(
          event.offsetX,
          event.offsetY,
          true
        )
        this.redraw()
      }
    },
    send () {
      const canvas = this.$refs.canvas
      const dataURL = canvas.toDataURL("image/png")
      this.$emit('stopdrawing', dataURL)
      this.draw.lastData = dataURL
    },
    reset () {
      this.resetCanvas()
      this.redraw()
    }
  },
  ready () {
      this.redraw()
  }
}
</script>
