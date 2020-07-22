<template>
  <div class="waiting-room" id="waiting-room">
      <NavBar></NavBar>
      <p class='description'>
        <br><br>
        Welcome!
        <br>
        <br>
        <!--Sessions are at {{n_sched_times}} timings daily.
        <br><br>
        Next session starts at:
        <br>
        {{time_sched}}
        <br><br-->
        The next meditation starts in:
        <br><br>
        <Timer class='timer-clock' :timeLimit='time_limit' @timer-expired='onTimerExpired'></Timer>
        <br>
        Remind me daily <!--input form: 8 AM ET, 8 PM ET, both (only if no cookie)-->
        <br><br>
        Check your settings in a quick demo:
        <br>
    </p>
    <p class='description'>
        <br><br>
        Joining in...
        <br><br>
        <Timer class='timer-clock' :timeLimit='time_limit' @timer-expired='onTimerExpired'></Timer>
        <br>
        Please wait here until the timer hits 0.
        <br>
        You will automatically join the session.
      </p>
  </div>
</template>
<script>
import Timer from '@/components/Timer'
import NavBar from '@/components/NavBar'
import router from '../router'
import NoSleep from 'nosleep.js';
export default {
  name: 'WaitingRoom',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      time_limit: 0,
      //time_sched: "N/A",
      //n_sched_times: 0
    }
  },
  components: {
    SessionTopBar,
    Timer,
    SessionBottomBar,
    NavBar
  },
  
  mounted() {

    document.body.style.backgroundColor = "#2AD9FF";

    //use or create id from cookie
    this.client_id = "fake";
    //console.log("cookies1:",this.$cookies);
    if (this.$cookies.isKey('medliveorg')) {
      this.client_id = this.$cookies.get('medliveorg');
      console.log(this.client_id,": found cookie");
    }
    else {
      this.client_id = Math.random().toString(36).slice(-5);
      this.$cookies.set('medliveorg',this.client_id,-1);
      console.log("create cookie");
    }


    this.fetch_time = '/api/timedata';
    var fetch_time_bool = true;
    if (this.$route.query.t) { //check if URL query given
      var time_query = this.$route.query.t;
      if (time_query.includes("-")) { //sched time given in query
        this.fetch_time += "?sched=" + time_query;
        console.log("fetch sched time:",this.fetch_time);
      }
      else {
        if (isNaN(parseInt(time_query))) { //time limit error
          console.log("could not parse time request");
        }
        else { //time limit given, no need to fetch time
          this.time_limit = parseInt(time_query);
          fetch_time_bool = false;
        }
      }
    }

    if (this.$route.query.f) { //if query given f=1, delete all active users
      if (this.$route.query.f == "1") {
        this.flushActiveUsersDB();
      }
    }

    //if need to get time data from backend
    if (fetch_time_bool) {
      this.timePassed = 0;
      this.refreshTimer();
      this.timerInterval = setInterval(() => this.refreshTimer(), 1000);
    }
  },

  beforeDestroy() {

    clearInterval(this.timerInterval); //stop refresh timer
    document.body.style.backgroundColor = "#FFFFFF";
    //this.lock.unlock();

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

    flushActiveUsersDB() { //delete all active users in DB
      fetch('api/flushactiveusersdb')
      .then(response => {
        if (response.status !== 200) { //server error handling
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(data => {

          console.log("time data:",data);
          if ('error' in data) { //error handling from testroom backend call
            //console.log(this.client_id,": flush active users DB error: ",data['error']);
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

    kickOutWaitingRoom() { //redirect to session end
      router.push({ name: "SessionEnd" });
    },

    requestRoom(testRoom) { //set up video chat room

      if (testRoom) {
        var entry = {
          clientID: this.client_id,
          testRoom: true
        };
      }
      else {
        var entry = {
          clientID: this.client_id
        };
      }

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
          //console.log("data: ",data);

          if ('error' in data) { //error handling from testroom backend call
            console.log(this.client_id,": requestroom error: ",data['error']);
            alert("requestroom error: " + data['error']);
            return;
          }

          var room_name = "hello"; //take room name from backend call
          if ('room_name' in data) { 
            room_name = data['room_name'];
            console.log(this.client_id,": room name: ",room_name);
          }

          if (testRoom) {
            console.log("passing test room name to call:",room_name);
            router.push({
              name: "Test",
              params: {
                roomName: room_name
              }
            })
          }
          else {

            var med_time = 0;
            if (this.$route.query.m) { //if query given m, set meditation duration
              let med_query = this.$route.query.m;
              if (isNaN(parseInt(med_query))) { //time limit error
                console.log("could not parse meditation time request");
              }
              else { //med time given
                med_time = parseInt(med_query);
              }
            }

            console.log("passing room name to call:",room_name);
            //take user to call page
            router.push({
              name: "Call",
              params: {
                roomName: room_name,
                medTime: med_time
              }
            })
          }
        });
      })
      .catch(error => { //error handling
        console.log("Fetch error: " + error);
      });
    },

    testSession() { //open private video chat room
      this.requestRoom(true);
    }, 

    onTimerExpired() { //loads meditation room when timer ends
      this.requestRoom();
    },

    refreshTimer() { //refresh timer every minute
    
      //console.log("time passed:",this.timePassed);

      if (this.timePassed % 60 == 0) {

        console.log("refresh time");

        fetch(this.fetch_time)
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

            //this.n_sched_times = parseInt(data['n_sched_times']);

            let time_diff = parseInt(data['time_diff']); //change to kick out flag
            if (time_diff > 0) {
              //this.time_limit = parseInt((time_sched - time_current)/1000);
              this.time_limit = time_diff;

              //let time_sched_min = String(data['sched_min']);
              //console.log("sched length:",time_sched_min.length)
              //if (time_sched_min.length == 1) {
              //  time_sched_min = '0' + time_sched_min;
              //}
              //let offset = new Date().getTimezoneOffset();
              //let time_zone = Intl.DateTimeFormat().resolvedOptions().timeZone
              //let sched_utc = new Date(data['time_sched']);
              //let sched_offset = new Date(sched_utc - 1000 * 60 * offset);
              //console.log("offset:",offset,", time zone:",time_zone,", sched utc:",sched_utc,", sched_offset:",sched_offset);
              //this.time_sched = sched_offset;
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
      this.timePassed += 1;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

html, body {
  height: 100%;
  margin: 0;
}

.waiting-room {
  /*font-family: 'DIN Condensed', sans-serif;*/
  font-size: 20px;
  background-color:#2AD9FF;
  color:#FFFFFF;
  line-height: 1.5;
  /*height: 100%;
  width: 100%;*/
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

.timer-clock {
  font-size: 36px;
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

  cursor: pointer;
  position: relative;
}

</style>
