<template>
  <div class="custom-menu" @mouseenter="focusSearch">
    <Menu
      ref="customMenu"
      :search-bar="true"
      :search-keep="(title) => ['Refresh'].includes(title)"
      :delay="100000"
      :style="style"
    />
  </div>
</template>

<script>
import { Menu } from 'rete-context-menu-plugin'
export default {
  components: {
    Menu
  },
  data () {
    return {
      x: -10000,
      y: -10000
    }
  },
  computed: {
    style () {
      if (this.x >= 0) {
        return {
          top: (this.y - 50) + 'px',
          left: (this.x + this.$refs.customMenu.$el.querySelector('.search input').offsetWidth / 2) + 'px'
        }
      }
      return {}
    }
  },
  methods: {
    focusSearch (evt) {
      this.$refs.customMenu.$el.querySelector('.search input').focus()
      if (this.x < 0 || this.y < 0) {
        this.x = evt.clientX
        this.y = evt.clientY
      }
    }
  }
}
</script>
