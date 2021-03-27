<template>
  <div :class="['remaining-time', {'disabled': disabled}]">
    <v-container>
      <v-row>
        <v-col>
          <v-sheet class="time-slot" :elevation="3">
            <div class="explanation" v-if="nextDate">
              Time until {{nextDate.toDate().toString().split(' ').splice(0, 5).join(' ')}}
              - Reocurring {{cronToText(cron)}} <span class="highlight cron">({{cron}})</span>
            </div>
            <div class="explanation" v-else>
              No schedule time is set for this dag, click on the pen in the top left corner to set one
            </div>
          </v-sheet>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="slot in timeSlots" :key="slot.name">
          <v-sheet :class="['time-slot', slot.name.toLowerCase()]" :elevation="3">
            {{slot.value}}
            <small class="explanation">{{slot.name}}</small>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import cronToText from 'cron-to-text'
import cronParser from 'cron-parser'

export default {
  props: {
    cron: String,
    disabled: Boolean
  },
  data () {
    return {
      interval: null,
      days: 0,
      hours: 0,
      minutes: 0,
      seconds: 0,
      nextDate: null,
      intervals: {
        second: 1000,
        minute: 1000 * 60,
        hour: 1000 * 60 * 60,
        day: 1000 * 60 * 60 * 24
      }
    }
  },
  computed: {
    timeSlots () {
      return [
        {
          name: 'DAYS',
          value: this.days
        },
        {
          name: 'HOURS',
          value: this.hours
        },
        {
          name: 'MINUTES',
          value: this.minutes
        },
        {
          name: 'SECONDS',
          value: this.seconds
        }
      ]
    }
  },
  methods: {
    cronToText,
    updateClock () {
      if (!this.cron) return
      const cronDate = cronParser.parseExpression(this.cron).next()
      this.nextDate = cronDate
      if (!this.disabled) {
        let diff = Math.abs(Date.now() - cronDate.getTime())
        this.days = Math.floor(diff / this.intervals.day)
        diff -= this.days * this.intervals.day
        this.hours = Math.floor(diff / this.intervals.hour)
        diff -= this.hours * this.intervals.hour
        this.minutes = Math.floor(diff / this.intervals.minute)
        diff -= this.minutes * this.intervals.minute
        this.seconds = Math.floor(diff / this.intervals.second)
      }
    }
  },
  created () {
    this.interval = setInterval(() => {
      this.updateClock()
    }, 1000)

    this.updateClock()
  },
  destroyed () {
    clearInterval(this.interval)
  }
}
</script>

<style scoped>
.remaining-time {
  font-size: 40pt;
  font-family: Roboto, sans-serif;
  /*
  background-image: url(../assets/gaming.png);
  background-size: 100% auto;
  background-position-y: 55%;
  */
}
.remaining-time .time-slot.seconds {
  color: #ee5486;
}
.remaining-time .time-slot {
  padding: 10px 0;
  text-align: center;
}
.remaining-time .time-slot .explanation {
  font-size: 15pt;
}
.remaining-time.disabled .time-slot {
  color: grey;
}

.highlight {
  background: rgba(255,255,255,0.1);
  padding: 5px;
  border-radius: 3px;
}
</style>
