<template>
  <div class="schedule-confirmation">
    <NavBar></NavBar>

    <p class='description'>
        It's set! You will receive an email 30 minutes before your session.
    </p>
    <div class='schedule-section'>
        <div class='schedule-time'></div>
    </div>
    <p class='description'>
        Want to do a test run?
    </p>
    <div class='test-session-button' v-on:click="testSession()">
        <p class='test-session-text'>
            Test Session
        </p>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar';
import router from '../router';
export default {
  name: 'ScheduleConfirmation',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    NavBar
  },
  methods: {
    testSession() {
      router.push({
        name: "Call",
        props: {
          testSession: true
        }
      })
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
