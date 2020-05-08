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
      const minutes = Math.floor(timeLeft / 60);
      let seconds = timeLeft % 60;

      if (seconds < 10) {
        seconds = `0${seconds}`;
      }

      return `${minutes}:${seconds}`;
    },

    timeLeft() {
      return this.timeLimit - this.timePassed;
    },

    timeFraction() {
      const rawTimeFraction = this.timeLeft / TIME_LEFT;
      return rawTimeFraction - (1 / this.timeLimit) * (1 - rawTimeFraction);
    }
  },

  watch: {
    timeLeft(newValue) {
      if (newValue === 0) {
        this.onTimesUp();
      }
    }
  },

  mounted() {
    this.startTimer();
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
