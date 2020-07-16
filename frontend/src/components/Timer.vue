<template>
  <div class="timer">
    {{ formattedTimeLeft }}
  </div>
</template>

<script>
export default {
  name: 'Timer',
  data () {
    return {
      timePassed: 0,
      timerInterval: null
    }
  },

  computed: {
    formattedTimeLeft() {
      const timeLeft = this.timeLeft;
      let minutes = Math.floor(timeLeft / 60);
      let hours = Math.floor(minutes / 60);
      minutes %= 60;
      let seconds = timeLeft % 60;

      hours = (hours == 0) ? '' : hours += ':'

      if (minutes < 10) {
        minutes = `0${minutes}`;
      }

      if (seconds < 10) {
        seconds = `0${seconds}`;
      }

      return `${hours}${minutes}:${seconds}`;
    },

    timeLeft() {
      return this.timeLimit - this.timePassed;
    }
  },

  watch: {
    timeLeft(newValue) {
      console.log("time left:",this.timeLeft);
      if (newValue == 0) {
        this.onTimesUp();
      }
    },

    timeLimit(newValue) {
      console.log("time limit:",this.timeLimit);
      this.startTimer();
      this.refreshTimer();
    }
  },

  methods: {
    onTimesUp() {
      clearInterval(this.timerInterval);
      this.$emit('timer-expired');
    },

    startTimer() {
      this.timePassed = 0;
      clearInterval(this.timerInterval);
      this.timerInterval = setInterval(() => (this.timePassed += 1), 1000);
    },

    refreshTimer() {
      //run in a loop
      //capture current time
      //cal end time = start time + time limit
      //when screen becomes active, check current time
      //every min, check current time
      //calc diff = end time - current time
      //set new timeLeft
    }
  },

  props: [
    'timeLimit'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
