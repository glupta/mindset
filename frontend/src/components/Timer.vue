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
      clearInterval(this.refreshInterval);
      this.$emit('timer-expired');
    },

    startTimer() {
      this.timePassed = 0;
      clearInterval(this.timerInterval);
      this.timerInterval = setInterval(() => (this.timePassed += 1), 1000);
    },

    refreshTimer() { //keeps timer in sync with server

      delete this.timeEnd; 
      this.getCurrentTime(); //set end time = current time + time limit

      //every min, set timeLeft = end time - current time
      clearInterval(this.refreshInterval);
      this.refreshInterval = setInterval(() => this.getCurrentTime(), 60000);

      //when screen becomes active, check current time
      document.addEventListener("visibilitychange",this.getCurrentTime);
    },

    getCurrentTime() { //get current time and update time left

      fetch('/api/timedata')
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {
          if ('error' in data) { //error handling from  backend call
            console.log(this.client_id,": request time error: ",data['error']);
            alert("request time error: " + data['error']);
            return;
          }
          this.timeCurrent = new Date(data['time_current']); //get current time
          if (this.timeEnd) { //update timeLeft if end time exists
            this.timeLeft = parseInt(this.timeEnd - this.timeCurrent) / 1000; 
            console.log("current:",this.timeCurrent,", left:",this.timeLeft);
          }
          else { //set end time if first refresh
            this.timeEnd = new Date(this.timeCurrent.getTime() + this.timeLimit * 1000);
            console.log("current:",this.timeCurrent,", end:",this.timeEnd);
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
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
