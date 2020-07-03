<template>
  <div class='session-top-bar'>
    <p class='session-time'>
      <!-- {{timerCopy}} -->
      <br>
      {{timeleftCopy}}
      <Timer :timeLimit="timeLimit" @timer-expired="onTimerExpired"></Timer>
    </p>
    <div class='session-status'>
      <p class='session-status-text'>
        <br>{{sessionCopy}}
      </p>
    </div>
    <!--div class='leave-button'>
      <p class='leave-text'>
        Leave
      </p>
    </div-->
  </div>
</template>

<script>
import Timer from '@/components/Timer'
export default {
  name: 'SessionTopBar',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      sessionCopy: '',
      timeLeftCopy: 'Time Left: '
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
    'timerCopy',
    'timeLimit',
    'sessionCopy'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.session-top-bar {
  height: 50px;
}

.session-time {
  float: left;
  font-size: 16px;

}

.session-status-text {
  font-size: 16px;
}

.leave-button {
  float: right;
  background-color:#18a0fb;
	border-radius:3px;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family: 'DIN Condensed', sans-serif;
}

</style>
