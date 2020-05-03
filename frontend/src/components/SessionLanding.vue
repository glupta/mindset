<template>
  <div class="session-landing">
    <NavBar></NavBar>
    <p class='header'>
      It's time!
    </p>
    <p class='description'>
      Join the waiting room and ensure your settings are
      good. Prepare your environment and state of mind.
    </p>
    <div class='cta' v-on:click="enterWaitingRoom()">
      <p>
        Enter Waiting Room
      </p
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import router from '../router'
export default {
  name: 'SessionLanding',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    NavBar
  },
  methods: {
    enterWaitingRoom() {
      router.push({ name: "WaitingRoom" })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
