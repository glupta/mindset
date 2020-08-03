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
      formattedTimeLeft: ''
    }
  },
  watch: {
    timeLimit(newValue) {
      this.startTimer();
      this.refreshTimer();
    },

    stopTimer(newValue) {
    	if (this.stopTimer) {
    		clearInterval(this.timerInterval);
      	clearInterval(this.refreshInterval);
    	}
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
      this.timeLeft = this.timeLimit;
      this.fiveTrigger();
      this.formatTimeLeft();
      clearInterval(this.timerInterval);
      clearInterval(this.refreshInterval);
      console.log("time limit:",this.timeLimit);
      this.timerInterval = setInterval(() => this.updateTimer(), 1000);
    },

    updateTimer() { //update clock every second
      this.timePassed += 1;
      this.timeLeft = this.timeLimit - this.timePassed;
      console.log("left:",this.timeLeft,"passed:",this.timePassed,"limit:",this.timeLimit);
      this.formatTimeLeft();
			this.fiveTrigger();
      if (this.timeLeft == 0) {
        this.onTimesUp();
      }
    },

    fiveTrigger() { //emits when less or more than 5 minutes
    	if (this.timeLeft <= 300 && !this.fiveBool) {
      	this.$emit('less-five');
      	this.fiveBool = true;
      }
      else if (this.timeLeft > 300 && this.fiveBool) {
      	this.$emit('more-five');
      	this.fiveBool = false;
      }
    },

    formatTimeLeft() { //creates string of time left
    	let minutes = Math.floor(this.timeLeft / 60);
      let hours = Math.floor(minutes / 60);
      minutes %= 60;
      let seconds = this.timeLeft % 60;
      hours = (hours == 0) ? '' : hours += ':';
      if (minutes < 10) {
        minutes = `0${minutes}`;
      }
      if (seconds < 10) {
        seconds = `0${seconds}`;
      }      
      this.formattedTimeLeft = hours + minutes + ':' + seconds;
    },

    refreshTimer() { //keeps timer in sync with server

      delete this.timeStart; 
      this.getCurrentTime(); //set start time = current time + time limit

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
          if (this.timeStart) { //update timeLeft if end time exists
            this.timePassed = Math.round(parseInt(this.timeCurrent - this.timeStart) / 1000); 
            console.log("start:",this.timeStart,"current:",this.timeCurrent,"passed:",this.timePassed);
          }
          else { //set end time if first refresh
            this.timeStart = this.timeCurrent;
            console.log("start:",this.timeStart);
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }
  },

  props: [
    'timeLimit',
    'stopTimer'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
