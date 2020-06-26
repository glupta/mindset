<template>
  <div class="waiting-room">
    <SessionTopBar :timeLimit=time_limit timerCopy='Session starts in ' v-on:timer-expired="onTimerExpired"></SessionTopBar>
    <div class='waiting-room-partner'>
        
        <p class='description' style='background-color:#2AD9FF;color:#FFFFFF;'>
        <br><br>
        You're here!
        <br><br>
        The next session is at:
        <br>
        {{time_sched}}
        <br><br><br>
        <!--input v-model="user_text" placeholder="Enter your name"></input-->
        Want to do a test run?
        <br><br>
        <a class='test-session-button' v-on:click="testSession()">Test Session</a>
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
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      time_sched: ""
    }
  },
  components: {
    SessionTopBar,
    SessionBottomBar
  },
  mounted() {

      this.client_id = "fake";
      console.log("cookies1:",this.$cookies);
      if (this.$cookies.isKey('medliveorg')) {
        this.client_id = this.$cookies.get('medliveorg');
        console.log("found cookie");
      }
      else {
        this.client_id = Math.random().toString(36).slice(-5);
        this.$cookies.set('medliveorg',this.client_id);
        console.log("added cookie");
      }
      console.log(this.client_id,": cookies2:",this.$cookies);


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
        let time_sched_month = (time_sched.getMonth()+1).toString();
        let time_sched_date = time_sched.getDate().toString();
        let time_sched_year = time_sched.getFullYear().toString();
        let time_sched_hour = time_sched.getHours().toString();
        let time_sched_min = time_sched.getMinutes().toString();
        if (time_sched.getMinutes() < 10)
          time_sched_min = "0" + time_sched_min;
        this.time_sched = time_sched_month + "/" + time_sched_date + "/" + time_sched_year + " " + time_sched_hour + ":" + time_sched_min + " UTC";
        console.log("current time1: ",time_current," sched time1:",time_sched);
      
        if (time_sched.getTime() < time_current.getTime()) { //reroute if user joined waiting room too late
          this.onWaitingRoomLate();
        } else {

          this.time_limit = parseInt((time_sched - time_current)/1000); //time until session starts
          //this.time_limit = 30;
          console.log("time limit:",this.time_limit);
        }
      });
    })
    .catch(error => { //error handling
      console.log("Fetch error: " + error);
    });
  },
  
  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'Waiting Room' || 'Some Default Title';
      }
    }
  },

  methods: {
    onWaitingRoomLate() {
      router.push({ name: "SessionEnd" });
    },
    testSession() {

      //create json data to send to server
      //send parameter: device/client ID
      var entry = {
        clientID: this.client_id
      };

      fetch('/api/testroom', {
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

          if ('error' in data) { //error handling from testroom backend call
            console.log(this.client_id,": requestroom error: ",data['error']);
            alert("requestroom error: " + data['error']);
            return;
          }

          var room_name = "hello"; //take room name from backend call
          if ('room_name' in data) { 
            room_name = data['room_name'];
            console.log(this.client_id,": test room name: ",room_name);
          }

          console.log("passing test room name to call:",room_name);
          //take user to call page
          router.push({
            name: "Call",
            params: {
              testSession: true,
              roomName: room_name
            }
          })
        })
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },
    onTimerExpired() {

      //create json data to send to server
      //send parameter: device/client ID
      var entry = {
        clientID: this.client_id
      };
      
      //call the backend to get assigned room
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

          if ('error' in data) { //error handling from requestroom backend call
            console.log(this.client_id,": requestroom error: ",data['error']);
            alert("requestroom error: " + data['error']);
            return;
          }

          var room_name = "hello"; //take room name from backend call
          if ('room_name' in data) { 
            room_name = data['room_name'];
            console.log(this.client_id,": room name: ",room_name);
          }

          console.log("passing room name to call:",room_name);
          //take user to call page
          router.push({
            name: "Call",
            params: {
              roomName: room__name
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

.test-session-button {
  font-size: 18px;
  font-family: 'DIN Condensed', sans-serif;
  border-radius: 5px;
  border: 2px solid #18A0FB;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 95px;
  padding-left: 95px;
  color: #18a0fb;
}
</style>
