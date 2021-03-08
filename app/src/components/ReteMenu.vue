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

<style>

.custom-menu .context-menu {
  left: 0;
  top: 0;
  position: absolute;
  padding: 10px;
  margin-top: -20px;
  width: auto !important;
}
.custom-menu .context-menu > .item, .custom-menu .context-menu > .search {
  margin-left: -80%;
}
.custom-menu .context-menu > .item .subitems {
  position: absolute;
  display: none;
  left: 100%;
  top: 0;
  border-radius: 7px;
  overflow: overlay;
}
.custom-menu .context-menu > .item:hover .subitems {
  display: block;
}
.custom-menu .context-menu > .item.have-subitems {
  padding-right: 16px;
}
.custom-menu .context-menu > .item.have-subitems:after {
  content: "►";
  position: absolute;
  opacity: 0.6;
  right: 5px;
  top: 5px;
}
.custom-menu .context-menu .item, .custom-menu .context-menu .search {
  padding: 4px !important;
  border-bottom: 1px solid rgba(15, 15, 15, 0.7) !important;
  color: #fff !important;
  background-color: rgba(35, 35, 35, 0.9) !important;
  cursor: pointer !important;
  width: auto !important;
  position: relative !important;
}
.custom-menu .context-menu .item:first-child {
  border-radius: 7px 7px 0 0;
}
.custom-menu .context-menu .item:last-child {
  border-radius: 0 0 7px 7px;
}
.custom-menu .context-menu .item:hover {
  background-color: rgba(45, 45, 45, 0.9) !important;
}
</style>
