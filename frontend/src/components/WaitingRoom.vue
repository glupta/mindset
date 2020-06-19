<template>
  <div class="waiting-room">
    <SessionTopBar :timeLimit=time_limit timerCopy='Session starts in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <div class='waiting-room-partner'>
        
        <p class='description' style='background-color:#2AD9FF;color:#FFFFFF;'>
        <br><br><br><br><br><br><br><br>
        You're here!
        <br>
        Waiting for your meditation<br>
        buddy to join.
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        <br><br><br><br><br><br><br>
        </p>
        
    </div>
    <div class='video-chat-self'></div>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>

<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar
  },
  mounted() {
    
    fetch('/api/timedetails') //calls backend to get time details
    .then(response => {
      if (response.status !== 200) { //server error handling
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(data => {
      
        let time_current = new Date(data["time_current"]);
        let time_sched = new Date(data["time_sched"]);
        console.log("current time1: ",time_current," sched time1:",time_sched);
      
        if (time_sched.getTime() < time_current.getTime()) { //check if user joined waiting room too late
          this.onWaitingRoomLate();
        } else {
          this.time_limit = parseInt((time_sched - time_current)/1000); //time until session starts
          console.log("time limit:",this.time_limit);
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },

  methods: {
    onWaitingRoomLate() {
      router.push({ name: "SessionEnd" })
    },
    onTimerExpired() {
      
      //create json data to send to server
      //send parameter: device/client ID (currently sending dummy data)
      var entry = {
        hello1: "hello1",
        hello2: "hello2"
      };
      
      //call the backend '/api/requestroom'
      fetch('/api/requestroom', {
        method: "POST",
        body: JSON.stringify(entry),
        headers: new Headers({
        "content-type": "application/json"
        })
      })
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {
          console.log(data);
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });

      router.push({ name: "Call" }) //take user to call page
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.waiting-room {
  font-family: 'DIN Condensed', sans-serif;
  font-size: 24px;
}
</style>
