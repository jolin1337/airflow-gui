<template>
  <v-app id="app">
    <v-app-bar app hide-on-scroll>
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>

      <v-toolbar-title>
        <router-link to="/">Airflow</router-link>
        <template v-if="dag"> - {{dag.dag_id}}</template>
        <template v-else-if="['/', '/dag'].includes($route.path)"> - DAGs</template>
        <template v-else> - {{navLinks.find(l => l.url === $route.path).name}}</template>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute temporary>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            Airflow
          </v-list-item-title>
          <v-list-item-subtitle>
            LTE webservice
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list nav dense>
        <template v-for="link in navLinks">
          <v-list-item @click="$router.push(link.url)" :key="link.name">
            <v-list-item-icon v-if="link.icon">
              <v-icon>{{link.icon}}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>{{link.name}}</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar color="cyan">
      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-toolbar-title></v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-toolbar>
    <router-view />
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data () {
    return {
      drawer: false,
      group: 'test',
      navLinks: [
        {
          url: '/',
          name: 'Home',
          icon: 'mdi-home'
        },
        {
          url: '/connections',
          name: 'Connections',
          icon: 'mdi-power-plug'
        },
        {
          url: '/variables',
          name: 'Variables',
          icon: 'mdi-variable'
        },
        {
          url: '/users',
          name: 'Users',
          icon: 'mdi-account'
        },
        {
          url: '/about',
          name: 'About',
          icon: 'mdi-information'
        }
      ]
    }
  },
  computed: {
    ...mapState({
      dag: state => {
        const sel = state.dags.selected || {}
        if (sel.runs) {
          return sel.runs
        }
        return sel.graph
      }
    })
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
#app a {
  color: white;
}
</style>
