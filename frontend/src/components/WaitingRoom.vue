<template>
  <div class="waiting-room">
    <!--SessionTopBar :timeLimit=time_limit @timer-expired="onTimerExpired"></SessionTopBar-->
    <div class='waiting-room-partner'>
      <NavBar></NavBar>
      <p class='description'>
        <br><br>
        Welcome!
        <br><br>
        <!--Sessions are at {{n_sched_times}} timings daily.
        <br><br>
        The next session starts at:
        <br>
        {{time_sched}}
        <br><br-->
        The next session starts in:
        <br>
        <Timer :timeLimit='time_limit' @timer-expired='onTimerExpired'></Timer>
        <br><br><br>
        Check your settings:
        <br>
        <button class='test-session-button' @click="testSession">Launch Test Session</button>
        <br><br><br><br><br><br><br><br><br><br>
      </p>
    </div>
    <div class='video-chat-self'></div>
    <SessionBottomBar></SessionBottomBar>
  </div>
</template>
<script>
import SessionTopBar from '@/components/SessionTopBar'
import Timer from '@/components/Timer'
import SessionBottomBar from '@/components/SessionBottomBar'
import NavBar from '@/components/NavBar'
import router from '../router'
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      time_sched: "N/A",
      n_sched_times: 0
    }
  },
  components: {
    SessionTopBar,
    Timer,
    SessionBottomBar,
    NavBar
  },

  onTimerExpired() {
      this.$emit('timer-expired');
  },
  
  mounted() {

    //this.$cookies.set('medliveorg-active',0);

    //use/create id from cookie
    this.client_id = "fake";
    console.log("cookies1:",this.$cookies);
    if (this.$cookies.isKey('medliveorg-clientID')) {
      this.client_id = this.$cookies.get('medliveorg-clientID');
      //this.clients_active = parseInt(this.$cookies.get('medliveorg-active'));
      //if (isNaN(this.clients_active)) {
      //  this.clients_active = 0;
      //}
      console.log(this.client_id,": found cookie"); //", active clients:",this.clients_active);
      if (this.clients_active > 0) {
        this.kickOutWaitingRoom();
      }
    }
    else {
      this.client_id = Math.random().toString(36).slice(-5);
      //this.clients_active = 0;
      this.$cookies.set('medliveorg-clientID',this.client_id);
      console.log("create cookie");
    }

    //this.clients_active += 1;
    //this.$cookies.set('medliveorg-active',this.clients_active);
    console.log(this.client_id,": cookies2:",this.$cookies);
    //console.log(this.client_id,": increment cookie, active clients:",this.clients_active);

    var fetch_time = '/api/timedata';
    var fetch_time_bool = true;
    if (this.$route.query.t) { //check if URL query given
      var time_query = this.$route.query.t;
      if (time_query.includes("-")) { //sched time given in query
        fetch_time += "?sched=" + time_query;
        console.log("fetch sched time:",fetch_time);
        this.flushActiveUsersDB();
      }
      else {
        if (isNaN(parseInt(time_query))) { //time limit error
          console.log("could not parse time request");
        }
        else { //time limit given, no need to fetch time
          this.time_limit = parseInt(time_query);
          fetch_time_bool = false;
          this.flushActiveUsersDB();
        }
      }
    }

    //if need to get time data from backend
    if (fetch_time_bool) {
      fetch(fetch_time)
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {

          console.log("time data:",data);
          if ('error' in data) { //error handling from testroom backend call
            console.log(this.client_id,": request time error: ",data['error']);
            alert("request time error: " + data['error']);
            return;
          }

          this.n_sched_times = parseInt(data['n_sched_times']);

          let time_diff = parseInt(data['time_diff']); //change to kick out flag
          if (time_diff > 0) {
            //this.time_limit = parseInt((time_sched - time_current)/1000);
            this.time_limit = time_diff;

            let time_sched_min = String(data['sched_min']);
            console.log("sched length:",time_sched_min.length)
            if (time_sched_min.length == 1) {
              time_sched_min = '0' + time_sched_min;
            }
            let offset = new Date().getTimezoneOffset();
            let time_zone = Intl.DateTimeFormat().resolvedOptions().timeZone
            let sched_utc = new Date(data['time_sched']);
            let sched_offset = new Date(sched_utc - 1000 * 60 * offset);
            console.log("offset:",offset,", time zone:",time_zone,", sched utc:",sched_utc,", sched_offset:",sched_offset);
            this.time_sched = sched_offset;
            // this.time_sched = time_sched_month + "/" + time_sched_date + "/" + time_sched_year + " " + time_sched_hour + ":" + time_sched_min + " UTC";
            //this.time_sched = data['sched_month'] + "/" + data['sched_day'] + "/" + data['sched_year'] + " " + data['sched_hour'] + ":" + time_sched_min + " UTC";
          }
          else { //kick out if current time is past sched time
            console.log("currently past sched time, kicking out");
            this.kickOutWaitingRoom();
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    }
  },

  //destroyed() {
    //this.clients_active -= 1;
    //this.$cookies.set('medliveorg-active',this.clients_active);
    //console.log(this.client_id,": decrement cookie, active clients:",this.clients_active);
  //},
  
  watch: { //set page title
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = 'Waiting Room' || 'Some Default Title';
      }
    }
  },

  methods: {
    flushActiveUsersDB() {
      fetch('api/flushactiveusersdb')
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {

          console.log("time data:",data);
          if ('error' in data) { //error handling from testroom backend call
            console.log(this.client_id,": flush active users DB error: ",data['error']);
            alert("flush active users DB error: " + data['error']);
            return;
          }

          if ('flush' in data) {
            console.log("flushed active users");
            return;
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    kickOutWaitingRoom() {
      router.push({ name: "SessionEnd" });
    },

    testSession() {

      //create json data to send to server
      //send parameter: device/client ID
      var entry = {
        clientID: this.client_id,
        testRoom: true
      };

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
            console.log(this.client_id,": request room error: ",data['error']);
            alert("request room error: " + data['error']);
            return;
          }

          this.room_name = "hello"; //take room name from backend call
          if ('room_name' in data) { 
            this.room_name = data['room_name'];
            console.log(this.client_id,": room name: ",this.room_name);
          }

          var med_time = 0;
          if (this.$route.query.m) { //check if URL query given for med time
            var med_query = parseInt(this.$route.query.m);
            console.log("med time given: ",med_query);
            if (!isNaN(parseInt(med_time))) { //time limit error
              med_time = med_query;
            }
          }

          console.log("passing room name to call:",this.room_name);
          //take user to call page
          router.push({
            name: "Call",
            params: {
              roomName: this.room_name,
              medTime: med_time
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
  /*font-family: 'DIN Condensed', sans-serif;*/
  font-size: 24px;
  background-color:#2AD9FF;
  color:#FFFFFF;
  line-height: 1.5;
}

.test-session-button {
  font-size: 18px;
  border-radius: 6px;
  border: 1px solid #18A0FB;
  /*
  font-family: 'DIN Condensed', sans-serif;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 40px;
  padding-left: 40px;
  */
  color: #FFFFFF;
  background-color: #18A0FB;

  box-sizing: border-box;
  line-height: 22px;
  width: 271px;
  height: 58px;

  cursor:pointer;
}

</style>
