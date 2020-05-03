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
.session-top-bar {
  height: 40px;
}

.session-time{
  float: left;
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
