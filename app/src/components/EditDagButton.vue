<template>
  <dialog-button
    fullscreen
    :action="validateSaveDag"
    dialog-title="Save and commit changes"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        style="background: #333"
        :elevation="3"
        v-bind="attrs"
        v-on="on"
      >
        <v-icon dark>mdi-pen</v-icon>
      </v-btn>
    </template>
    <v-textarea
      color="secondary"
      label="DAG Description"
      v-model="dag.description"
    ></v-textarea>
    <h1 class="title white--text mb-2">DAG Schedule interval</h1>
    <v-select
      color="secondary"
      item-color="secondary"
      :items="['hours', 'days', 'weeks', 'months']"
      label="Interval Type"
      v-model="intervalType"
    >
      <template v-slot:prepend>
        <v-text-field
          v-model="interval"
          style="margin-top: -16px"
          color="secondary"
          label="Repeat interval"
          type="number"
          :value="1"
        >
        </v-text-field>
      </template>
    </v-select>
    Repeat on:
    <template v-if="['weeks'].includes(intervalType)">
      <h2 class="title mb-2">Day of Week</h2>
      <v-chip-group multiple active-class="yellow--text darken-2" v-model="dow">
        <template v-for="tag in daysOfWeek">
          <v-chip :key="tag" v-if="tag < weekDays.length">
            {{ weekDays[tag] }}
          </v-chip>
        </template>
      </v-chip-group>
    </template>
    <template v-if="['months'].includes(intervalType)">
      <h2 class="title mb-2">Day of Month</h2>
      <v-chip-group multiple active-class="yellow--text darken-2" v-model="dom">
        <v-chip v-for="tag in daysOfMonth" :key="tag">
          {{ tag + 1 }}
        </v-chip>
      </v-chip-group>
    </template>
    <template v-if="['days', 'weeks', 'months'].includes(intervalType)">
      <h2 class="title mb-2">Hour of Day</h2>
      <v-chip-group multiple active-class="yellow--text darken-2" v-model="hod">
        <v-chip v-for="tag in hours" :key="tag">
          {{ tag + 1 }}
        </v-chip>
      </v-chip-group>
    </template>
    <template
      v-if="['hours', 'days', 'weeks', 'months'].includes(intervalType)"
    >
      <h2 class="title mb-2">Minute</h2>
      <v-chip-group multiple active-class="yellow--text darken-2" v-model="moh">
        <template v-for="tag in this.minutes">
          <v-chip :key="tag" v-if="(tag + 1) % 5 === 0">
            {{ tag + 1 }}
          </v-chip>
        </template>
      </v-chip-group>
    </template>
    <v-spacer vertical></v-spacer>
    <v-container>
      Cron Expresson: <span class="highlight">{{ cron }}</span>
    </v-container>
    <h1 class="title white--text mb-2">Commit message</h1>
    <v-checkbox
      color="yellow darken-2"
      label="Create pull request in Kirby"
      v-model="createPR"
    ></v-checkbox>
    <v-textarea
      color="secondary"
      label="Message"
      v-model="commitMessage"
      counter
      :rules="[rules.length(20)]"
    ></v-textarea>
    <template v-slot:actions="{ confirmAction }">
      <v-btn
        color="secondary"
        text
        v-if="!dag.is_paused"
        @click="toggleDagPaused()"
      >
        Pause DAG
      </v-btn>
      <v-btn color="secondary" text v-else @click="toggleDagPaused()">
        Resume DAG
      </v-btn>
      <v-btn color="secondary" text @click="confirmAction">
        Save &amp; commit
      </v-btn>
    </template>
  </dialog-button>
</template>

<script>
import DialogButton from '@/components/DialogButton'
import cronParser from 'cron-parser'

export default {
  components: {
    DialogButton
  },
  props: {
    value: Object
  },
  computed: {
    dag () { return this.value },
    weekDays () {
      return ['Monday', 'Tuesday', 'Wensday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    },
    daysOfMonth () {
      return this.numbers.slice(1, 32)
    },
    daysOfWeek () {
      return this.numbers.slice(0, 8)
    },
    hours () {
      return this.numbers.slice(0, 24)
    },
    minutes () {
      return this.numbers.slice(0, 60)
    },
    months () {
      return this.numbers.slice(1, 13)
    },
    cron () {
      const fields = {
        dayOfMonth: this.dom.length !== 0 ? this.dom.map(d => d + 1) : this.daysOfMonth,
        dayOfWeek: this.dow.length !== 0 ? this.dow : this.daysOfWeek,
        hour: this.hod.length !== 0 ? this.hod.map(h => (h + 1) % 24) : this.hours,
        minute: this.moh.length !== 0 ? this.moh.map(m => ((m + 1) * 5) % 60) : this.minutes,
        month: this.months,
        second: [0]
      }
      switch (this.intervalType) {
        case 'months':
          fields.month = this.months.filter(d => (d + 1) % this.interval === 0)
          break
        case 'weeks':
          fields.dayOfMonth = this.daysOfMonth.filter(d => (d + 1) % (7 * this.interval) === 0)
          fields.month = this.months
          break
        case 'days':
          fields.dayOfMonth = this.daysOfMonth.filter(d => (d + 1) % this.interval === 0)
          fields.month = this.months
          break
        case 'hours':
          fields.hour = this.hours.filter(h => ((h + 1) % 24) % this.interval === 0)
          fields.dayOfWeek = this.daysOfWeek
          fields.dayOfMonth = this.daysOfMonth
          fields.month = this.months
          break
        default:
          break
      }
      const cronExpression = cronParser.fieldsToExpression(fields).stringify()
      return cronExpression
    }
  },
  methods: {
    validateSaveDag () {
      this.dag.schedule_interval = `"${this.cron}"`
      const msg = {
        dag: this.dag,
        commitMessage: this.commitMessage,
        createPR: this.createPR
      }
      this.$emit('input', msg)
    },
    toggleDagPaused () {
      // TODO: Call to pause dag action in vuex
    }
  },
  watch: {
    'dag.schedule_interval' () {
      let cron = this.dag.schedule_interval
      if (cron.startsWith('"') && cron.endsWith('"')) {
        cron = cron.slice(1, -1)
      } else {
        return
      }
      const cronFields = cronParser.parseExpression(cron).fields
      this.moh = cronFields.minute.map(m => m === 0 ? 60 : parseInt(m / 5) - 1)
      this.hod = cronFields.hour.map(h => h === 0 ? 24 : h - 1)
      this.dow = cronFields.dayOfWeek
      this.dom = cronFields.dayOfMonth.map(d => d === 0 ? 31 : d - 1)
      if (this.dow.length !== this.daysOfWeek.length) {
        this.intervalType = 'weeks'
      } else if (this.dom.length !== this.daysOfMonth.length) {
        this.intervalType = 'months'
      } else if (this.hod.length !== this.hours.length) {
        this.intervalType = 'days'
      } else if (this.moh.length !== this.minutes.length) {
        this.intervalType = 'hours'
      }
    }
  },
  data () {
    return {
      rules: {
        length: len => v => (v || '').length <= len || `Warning, recommended commit messages are max ${len} characters`
      },
      commitMessage: '',
      createPR: false,
      numbers: Array.from(Array(100).keys()),
      intervalType: 'days',
      interval: 1,
      moh: [],
      hod: [],
      dow: [],
      dom: []
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
.highlight {
  background: rgba(255, 255, 255, 0.1);
  padding: 5px;
  border-radius: 3px;
}
</style>
