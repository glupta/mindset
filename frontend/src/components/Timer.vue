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
      minutes = minutes % 60;
      let seconds = timeLeft % 60;

      if (hours == 0) {
        hours = '';
      }
      else {
        hours += ':';
      }

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
      console.log("time left:",this.timeLeft)
      if (newValue <= 0) {
        this.onTimesUp();
      }
    },

    timeLimit(newValue) {
      this.timePassed = 0;
      this.startTimer();
    }
  },

  methods: {
    onTimesUp() {
      clearInterval(this.timerInterval);
      this.$emit('timer-expired');
    },

    startTimer() {
      this.timerInterval = setInterval(() => (this.timePassed += 1), 1000);
    }
  },

  props: [
    'timeLimit'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.timer {
  float:left;
}
</style>
