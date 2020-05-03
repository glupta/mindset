<template>
  <div class='session-top-bar'>
        <p class='session-time'>
            {{timerCopy}}
        </p>
        <Timer v-on:timer-expired="onTimerExpired"></Timer>
        <div class='leave-button'>
            <p class='leave-text'>
            Leave
            </p>
        </div>
    </div>
</template>

<script>
import Timer from '@/components/Timer'
export default {
  name: 'SessionTopBar',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    Timer
  },
  methods: {
    onTimerExpired() {
      this.$emit('timer-expired');
    }
  },
  props: [
    'timerCopy'
  ]
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
