<template>
  <div class="waiting-room">
    <SessionTopBar :timeLimit=time_limit timerCopy='Session starts in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <div class='waiting-room-partner'>
        
        <p class='description' style='background-color:#2AD9FF;color:#FFFFFF;'>
        <br><br>
        You're here!
        <br>
        Waiting for the session to start...
        <br><br>

        <!--select v-model="user_selection">
          <option disabled selected>Pick User</option>
          <option>User1</option>
          <option>User2</option>
          <option>User3</option>
          <option>User4</option>
        </select-->

        <input v-model="user_text" placeholder="Enter your name"></input>
        <br><br><br>

        </p>
        
    </div>
    <div class='video-chat-self'></div>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>
<script src="https://cdnjs.com/libraries/fingerprintjs2"></script>
<script>
import SessionTopBar from '@/components/SessionTopBar'
import SessionBottomBar from '@/components/SessionBottomBar'
import router from '../router'
import Fingerprint2 from 'fingerprintjs2'
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      user_selection: null,
      user_text: null
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
      
        //get current and scheduled times
        let time_current = new Date(data["time_current"]);
        let time_sched = new Date(data["time_sched"]);
        console.log("current time1: ",time_current," sched time1:",time_sched);
      
        if (time_sched.getTime() < time_current.getTime()) { //reroute if user joined waiting room too late
          this.onWaitingRoomLate();
        } else {
          this.time_limit = parseInt((time_sched - time_current)/1000); //time until session starts
          //this.time_limit = 10
          console.log("time limit:",this.time_limit);
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },

  watch: {
    user_selection(newValue) {
      console.log("user_selection is:",this.user_selection);
    },
    user_text(newValue){
      console.log("user_text is:",this.user_text);
    }
  },

  methods: {
    onWaitingRoomLate() {
      router.push({ name: "SessionEnd" });
    },
    onTimerExpired() {
      

          //fingerprinting to create unique client ID
          // if (window.requestIdleCallback) {
          //   requestIdleCallback(function () {
          //     Fingerprint2.get(function (components) {
          //       console.log(components) // an array of components: {key: ..., value: ...}
          //     })
          //   })
          // } else {
          //   setTimeout(function () {
          //     Fingerprint2.get(function (components) {
          //       console.log(components) // an array of components: {key: ..., value: ...}
          //     })  
          //   }, 500)
          // }

      //create json data to send to server
      //send parameter: device/client ID
      var entry = {
        //clientID: this.user_selection
        clientID: this.user_text
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
        response.json().then(data => { //info about client added to active users in DB
          console.log("data: ",data);
          //this.room_name = data['room_name'];

          var room_name = ""; //take room name from backend call
          if ('room_name' in data) {
            room_name = data['room_name'];
            console.log("room name: ",room_name);
          }

          //dummy data
          // if (this.user_selection == "User1" || this.user_selection == "User2")
          //   room_name = "room1";
          // else if (this.user_selection == "User3" || this.user_selection == "User4")
          //   room_name = "room2";

          //join video chat room (break into its own file)
          var room_url = "https://meditate-live.daily.co/";
          //room_url += room_name == "" ? 'hello' : room_name;
          if (room_name === "") {
            room_url += 'hello';
          } else {
            room_url += room_name;
          }

          console.log("passing URL to call:",room_url);
          //take user to call page
          router.push({
            name: "Call",
            params: {
              roomURL: room_url
            }
          })
        })
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
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
